from datetime import date, datetime
from typing import Dict, List, Optional, Tuple

from PySide6.QtCore import Signal, QObject
import numpy as np
from dateutil.relativedelta import relativedelta
from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver.routing_enums_pb2 import (
    FirstSolutionStrategy,
    LocalSearchMetaheuristic,
)
from sklearn.cluster import DBSCAN
from sqlalchemy import func
from sqlalchemy.orm import joinedload

from common.model.column_types.point import Coordinate
from common.utils.number import NumberUtils
from db import Database
from domain.driver.model import Driver
from domain.roadmap.model import Roadmap
from domain.scheduling.model import Scheduling
from domain.vehicle.model import Vehicle
from factory.client.google_maps import GoogleMapsClientFactory


class RoadmapOptimizer(QObject):
    status_updated = Signal(str)

    def __init__(
        self,
        date: date,
        vehicles_relation: List[Vehicle],
        drivers_relation: List[Driver],
        on_call_driver_ids: List[int],
        departure_coordinates: Coordinate,
        dbscan_epsilon: float = 0.5,
        dbscan_min_samples: int = 2,
    ) -> None:
        super().__init__()
        self.__date = date
        self.__vehicles_relation = vehicles_relation
        self.__drivers_relation = drivers_relation
        self.__on_call_driver_ids = on_call_driver_ids
        self.__departure_coordinates = departure_coordinates
        self.__dbscan_epsilon = dbscan_epsilon
        self.__dbscan_min_samples = dbscan_min_samples

        self.__google_maps_client = GoogleMapsClientFactory.create()
        self.__schedulings: List[Scheduling] = []
        self.__used_vehicles: set = set()
        self.__driver_schedules: Dict[int, List[Dict]] = {}

    def __log(self, message: str) -> None:
        self.status_updated.emit(message)

    def generate_roadmaps(self) -> List[Roadmap]:
        """Método principal que gera os roadmaps usando DBSCAN + VRPTW."""
        self.__log("Iniciando otimização de roteiros...")
        self.__load_schedulings_for_date()
        self.__load_travel_time_matrix()
        clusters = self.__perform_dbscan_clustering()
        roadmaps = self.__process_clusters_with_vrptw(clusters)
        roadmaps = self.__assign_drivers_to_roadmaps(roadmaps)
        self.__log("Roteiros gerados com sucesso!")
        return roadmaps

    def __load_schedulings_for_date(self) -> None:
        with Database.session_scope(end_with_commit=False) as session:
            self.__schedulings = (
                session.query(Scheduling)
                .filter(func.date(Scheduling.datetime) == self.__date)
                .filter(Scheduling.roadmap_id.is_(None))
                .options(joinedload(Scheduling.location))
                .options(joinedload(Scheduling.patient))
                .options(joinedload(Scheduling.companions))
                .all()
            )
        if not self.__schedulings:
            raise ValueError("Nenhum agendamento encontrado para o dia selecionado.")

    def __load_travel_time_matrix(self) -> None:
        total_locations = len(self.__schedulings) + 1
        self.__travel_times_matrix = np.zeros((total_locations, total_locations))

        locations = [self.__departure_coordinates] + [
            scheduling.location.coordinates for scheduling in self.__schedulings
        ]

        count = 0
        total = total_locations**2

        for i, location in enumerate(locations):
            for j, other_location in enumerate(locations):
                if i < j:
                    travel_time = self.__google_maps_client.get_travel_time_between(
                        location, other_location
                    )
                    self.__travel_times_matrix[i, j] = travel_time
                elif i > j:
                    self.__travel_times_matrix[i, j] = self.__travel_times_matrix[j, i]

                count += 1
                progress = NumberUtils.float_to_str(int(count / total * 10000) / 100)
                self.__log(f"Calculando matriz de distâncias ({progress}%)...")

    def __perform_dbscan_clustering(self) -> Dict[int, List[Scheduling]]:
        if len(self.__schedulings) <= 1:
            return {0: self.__schedulings}

        self.__log("Agrupando agendamentos por similaridade de espaço e tempo...")

        clustering_data = []
        for scheduling in self.__schedulings:
            lat = (
                scheduling.location.coordinates.latitude
                + self.__departure_coordinates.latitude
            ) * 10
            lon = (
                scheduling.location.coordinates.longitude
                + self.__departure_coordinates.longitude
            ) * 10
            hour_normalized = (
                scheduling.datetime.hour * 60 + scheduling.datetime.minute
            ) / 30
            clustering_data.append([lat, lon, hour_normalized])

        clustering_data = np.array(clustering_data)

        dbscan = DBSCAN(
            eps=self.__dbscan_epsilon, min_samples=self.__dbscan_min_samples
        )
        cluster_labels = dbscan.fit_predict(clustering_data)

        clusters: Dict[int, List[Scheduling]] = {}
        for i, label in enumerate(cluster_labels):
            if label not in clusters:
                clusters[label] = []
            clusters[label].append(self.__schedulings[i])

        final_clusters = {}
        cluster_id = 0

        count = 0
        total = len(clusters)
        for label, schedulings in clusters.items():
            count += 1
            progress = NumberUtils.float_to_str(int(count / total * 10000) / 100)
            self.__log(f"Processando agrupamentos ({progress}%)...")
            if label == -1:
                for scheduling in schedulings:
                    final_clusters[cluster_id] = [scheduling]
                    cluster_id += 1
            else:
                sensitive_schedulings = [s for s in schedulings if s.sensitive_patient]
                normal_schedulings = [s for s in schedulings if not s.sensitive_patient]

                for scheduling in sensitive_schedulings:
                    final_clusters[cluster_id] = [scheduling]
                    cluster_id += 1

                if normal_schedulings:
                    final_clusters[cluster_id] = normal_schedulings
                    cluster_id += 1

        return final_clusters

    def __process_clusters_with_vrptw(
        self, clusters: Dict[int, List[Scheduling]]
    ) -> List[Roadmap]:
        all_roadmaps = []

        count = 0
        total = len(clusters)
        for _, schedulings in clusters.items():
            count += 1
            progress = NumberUtils.float_to_str(int(count / total * 10000) / 100)
            self.__log(f"Executando otimização dos agrupamentos ({progress}%)...")

            if len(schedulings) == 1:
                roadmap = self.__create_single_scheduling_roadmap(schedulings[0])
                all_roadmaps.append(roadmap)
            else:
                cluster_roadmaps = self.__solve_vrptw_for_cluster(schedulings)
                if len(cluster_roadmaps) > 0:
                    all_roadmaps.extend(cluster_roadmaps)

        return all_roadmaps

    def __create_single_scheduling_roadmap(self, scheduling: Scheduling) -> Roadmap:
        vehicle = self.__select_best_available_vehicle(scheduling)
        if not vehicle:
            raise ValueError(
                f"AVISO: Nenhum veículo disponível para agendamento {scheduling.datetime}"
            )

        scheduling_idx = self.__schedulings.index(scheduling)
        travel_time_to = self.__travel_times_matrix[0, scheduling_idx + 1]
        travel_time_from = self.__travel_times_matrix[scheduling_idx + 1, 0]

        arrival_at_scheduling = scheduling.datetime - relativedelta(minutes=15)
        departure_time = arrival_at_scheduling - relativedelta(
            seconds=int(travel_time_to)
        )

        return_start = scheduling.datetime + relativedelta(
            hours=scheduling.average_duration.hour,
            minutes=scheduling.average_duration.minute,
        )
        arrival_time = return_start + relativedelta(seconds=int(travel_time_from))

        self.__used_vehicles.add(vehicle.id)

        roadmap = Roadmap(
            driver_id=vehicle.default_driver_id,
            vehicle_id=vehicle.id,
            departure=self.__normalize_datetime(departure_time),
            arrival=self.__normalize_datetime(arrival_time),
        )
        roadmap.schedulings = [scheduling]

        return roadmap

    def __solve_vrptw_for_cluster(self, schedulings: List[Scheduling]) -> List[Roadmap]:
        if not schedulings:
            return []

        scheduling_indices = [self.__schedulings.index(s) + 1 for s in schedulings]
        num_locations = len(scheduling_indices) + 1

        available_vehicles = self.__get_available_vehicles_for_cluster(schedulings)
        if not available_vehicles:
            raise ValueError(
                f"AVISO: Nenhum veículo disponível para cluster com {len(schedulings)} agendamentos"
            )

        num_vehicles = min(len(schedulings), len(available_vehicles))

        location_indices = [0] + scheduling_indices
        travel_matrix = np.zeros((num_locations, num_locations))
        for i in range(num_locations):
            for j in range(num_locations):
                travel_matrix[i, j] = self.__travel_times_matrix[
                    location_indices[i], location_indices[j]
                ]

        manager = pywrapcp.RoutingIndexManager(num_locations, num_vehicles, 0)
        routing = pywrapcp.RoutingModel(manager)

        def time_callback(from_index, to_index):
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return int(travel_matrix[from_node, to_node])

        transit_callback_index = routing.RegisterTransitCallback(time_callback)
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        def demand_callback(from_index):
            from_node = manager.IndexToNode(from_index)
            if from_node == 0:
                return 0
            scheduling_idx = scheduling_indices[from_node - 1] - 1
            scheduling: Scheduling = self.__schedulings[scheduling_idx]
            return scheduling.get_passenger_count()

        demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)

        vehicle_capacities = [v.capacity for v in available_vehicles[:num_vehicles]]
        routing.AddDimensionWithVehicleCapacity(
            demand_callback_index,
            0,
            vehicle_capacities,
            True,
            "Capacity",
        )

        routing.AddDimension(
            transit_callback_index,
            3600,
            86400,
            False,
            "Time",
        )
        time_dimension = routing.GetDimensionOrDie("Time")

        for i, scheduling_idx in enumerate(scheduling_indices):
            index = manager.NodeToIndex(i + 1)
            scheduling = self.__schedulings[scheduling_idx - 1]

            scheduling_time_seconds = (
                scheduling.datetime.hour * 3600
                + scheduling.datetime.minute * 60
                + scheduling.datetime.second
            )

            earliest_arrival = max(0, scheduling_time_seconds - 90 * 60)  # 1h30 antes
            latest_arrival = scheduling_time_seconds - 15 * 60  # 15 min antes

            min_travel_time = int(self.__travel_times_matrix[0, scheduling_idx])
            earliest_arrival = max(earliest_arrival, min_travel_time)

            time_dimension.CumulVar(index).SetRange(earliest_arrival, latest_arrival)

        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (
            FirstSolutionStrategy.PATH_CHEAPEST_ARC
        )
        search_parameters.local_search_metaheuristic = (
            LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
        )
        search_parameters.time_limit.seconds = 30

        solution = routing.SolveWithParameters(search_parameters)
        if not solution:
            raise ValueError(
                f"AVISO: Não foi possível resolver VRPTW para cluster com {len(schedulings)} agendamentos"
            )

        roadmaps = []
        for vehicle_idx in range(num_vehicles):
            index = routing.Start(vehicle_idx)
            route_schedulings = []

            while not routing.IsEnd(index):
                node_index = manager.IndexToNode(index)
                if node_index > 0:
                    scheduling_idx = scheduling_indices[node_index - 1] - 1
                    route_schedulings.append(self.__schedulings[scheduling_idx])
                index = solution.Value(routing.NextVar(index))

            if route_schedulings:
                vehicle = available_vehicles[vehicle_idx]
                roadmap = self.__create_roadmap_from_route(route_schedulings, vehicle)
                roadmaps.append(roadmap)
                self.__used_vehicles.add(vehicle.id)

        return roadmaps

    def __get_available_vehicles_for_cluster(
        self, schedulings: List[Scheduling]
    ) -> List[Vehicle]:
        max_capacity_needed = max(s.get_passenger_count() for s in schedulings)

        available_vehicles = [
            v
            for v in self.__vehicles_relation
            if v.capacity >= max_capacity_needed and v.id not in self.__used_vehicles
        ]

        def vehicle_priority(vehicle: Vehicle) -> Tuple[int, int]:
            has_default_driver = 1 if vehicle.default_driver_id else 0
            return (has_default_driver, -vehicle.capacity)

        return sorted(available_vehicles, key=vehicle_priority, reverse=True)

    def __select_best_available_vehicle(
        self, scheduling: Scheduling
    ) -> Optional[Vehicle]:
        required_capacity = scheduling.get_passenger_count()

        available_vehicles = [
            v
            for v in self.__vehicles_relation
            if v.capacity >= required_capacity and v.id not in self.__used_vehicles
        ]

        if not available_vehicles:
            return None

        def vehicle_priority(vehicle: Vehicle) -> Tuple[int, int]:
            has_default_driver = 1 if vehicle.default_driver_id else 0
            return (has_default_driver, -vehicle.capacity)

        return sorted(available_vehicles, key=vehicle_priority, reverse=True)[0]

    def __create_roadmap_from_route(
        self, schedulings: List[Scheduling], vehicle: Vehicle
    ) -> Roadmap:
        schedulings.sort(key=lambda s: s.datetime)

        first_scheduling = schedulings[0]
        last_scheduling = schedulings[-1]

        first_arrival = first_scheduling.datetime - relativedelta(minutes=15)
        first_scheduling_idx = self.__schedulings.index(first_scheduling)
        travel_time_to_first = self.__travel_times_matrix[0, first_scheduling_idx + 1]

        if len(schedulings) > 1:
            travel_time_to_first += (
                (len(schedulings) - 1) * 10 * 60
            )

        departure_time = first_arrival - relativedelta(
            seconds=int(travel_time_to_first)
        )

        last_end = last_scheduling.datetime + relativedelta(
            hours=last_scheduling.average_duration.hour,
            minutes=last_scheduling.average_duration.minute,
        )
        last_scheduling_idx = self.__schedulings.index(last_scheduling)
        travel_time_from_last = self.__travel_times_matrix[last_scheduling_idx + 1, 0]
        arrival_time = last_end + relativedelta(seconds=int(travel_time_from_last))

        roadmap = Roadmap(
            driver_id=vehicle.default_driver_id,
            vehicle_id=vehicle.id,
            departure=self.__normalize_datetime(departure_time),
            arrival=self.__normalize_datetime(arrival_time),
        )
        roadmap.schedulings = schedulings

        return roadmap

    def __assign_drivers_to_roadmaps(self, roadmaps: List[Roadmap]) -> List[Roadmap]:
        self.__log("Atribuindo motoristas aos roteiros que não possuem um...")
        self.__driver_schedules = {driver.id: [] for driver in self.__drivers_relation}

        for roadmap in roadmaps:
            if roadmap.driver_id:
                self.__driver_schedules[roadmap.driver_id].append(
                    {"start": roadmap.departure, "end": roadmap.arrival}
                )

        regular_drivers = [
            d for d in self.__drivers_relation if d.id not in self.__on_call_driver_ids
        ]
        on_call_drivers = [
            d for d in self.__drivers_relation if d.id in self.__on_call_driver_ids
        ]

        roadmaps_without_driver = [r for r in roadmaps if not r.driver_id]
        roadmaps_without_driver.sort(key=lambda r: r.departure)

        for roadmap in roadmaps_without_driver:
            assigned_driver = None

            assigned_driver = self.__find_best_available_driver(
                roadmap, regular_drivers
            )

            if not assigned_driver:
                assigned_driver = self.__find_best_available_driver(
                    roadmap, on_call_drivers
                )

            if assigned_driver:
                roadmap.driver_id = assigned_driver.id
                self.__driver_schedules[assigned_driver.id].append(
                    {"start": roadmap.departure, "end": roadmap.arrival}
                )

        return roadmaps

    def __find_best_available_driver(
        self, roadmap: Roadmap, drivers: List[Driver]
    ) -> Optional[Driver]:
        available_drivers = []

        for driver in drivers:
            if self.__is_driver_available(roadmap, driver.id):
                available_drivers.append(driver)

        if not available_drivers:
            return None

        return min(available_drivers, key=lambda d: len(self.__driver_schedules[d.id]))

    def __is_driver_available(self, roadmap: Roadmap, driver_id: int) -> bool:
        driver_occupied_times = self.__driver_schedules.get(driver_id, [])

        for occupied_time in driver_occupied_times:
            if not (
                roadmap.arrival <= occupied_time["start"]
                or roadmap.departure >= occupied_time["end"]
            ):
                return False

        return True

    def __normalize_datetime(self, dt: datetime) -> datetime:
        return datetime(
            year=self.__date.year,
            month=self.__date.month,
            day=self.__date.day,
            hour=dt.hour,
            minute=dt.minute,
            second=dt.second,
        )
