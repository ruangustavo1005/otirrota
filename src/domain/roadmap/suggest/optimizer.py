from datetime import date, datetime
from typing import Dict, List

import numpy
from dateutil.relativedelta import relativedelta
from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver.routing_enums_pb2 import (
    FirstSolutionStrategy,
    LocalSearchMetaheuristic,
)
from sklearn.cluster import DBSCAN

from common.model.column_types.point import Coordinate
from db import Database
from domain.driver.model import Driver
from domain.roadmap.model import Roadmap
from domain.scheduling.model import Scheduling
from domain.vehicle.model import Vehicle
from factory.client.google_maps import GoogleMapsClientFactory


class RoadmapOptimizer:
    __travel_times_matrix: Dict[int, Dict[int, int]]

    def __init__(
        self,
        date: date,
        vehicles_relation: List[Vehicle],
        drivers_relation: List[Driver],
        on_call_driver_ids: List[int],
        departure_coordinates: Coordinate,
        dbscan_epsilon: float,
        dbscan_min_samples: int,
    ) -> None:
        self.__date = date
        self.__vehicles_relation = self.__sort_vehicles_by_priority(
            vehicles_relation, on_call_driver_ids
        )
        self.__drivers_relation = drivers_relation
        self.__on_call_driver_ids = on_call_driver_ids
        self.__departure_coordinates = departure_coordinates
        self.__dbscan_epsilon = dbscan_epsilon
        self.__dbscan_min_samples = dbscan_min_samples

        self.__google_maps_client = GoogleMapsClientFactory.create()

    def __sort_vehicles_by_priority(
        self, vehicles: List[Vehicle], on_call_driver_ids: List[int]
    ) -> List[Vehicle]:
        def get_vehicle_priority(vehicle: Vehicle) -> int:
            if vehicle.default_driver_id is None:
                return 2
            elif vehicle.default_driver_id in on_call_driver_ids:
                return 1
            return 0

        return sorted(vehicles, key=get_vehicle_priority)

    def generate_roadmaps(self) -> List[Roadmap]:
        self.__load_schedulings_for_date()
        self.__load_travel_time_between_locations()
        self.__clusterize_schedulings_by_space_and_time()
        roadmaps: List[Roadmap] = []
        for cluster in self.__schedulings_clusters:
            roadmaps.extend(self.__run_vrptw_for_cluster(cluster))
        roadmaps.sort(key=lambda r: r.departure)
        roadmaps = self.__assign_drivers_to_roadmaps_without_it(roadmaps)
        return roadmaps

    def __load_schedulings_for_date(self) -> None:
        with Database.session_scope(end_with_commit=False) as session:
            self.__schedulings = (
                session.query(Scheduling)
                .filter(Scheduling.datetime.cast("date") == self.__date)
                .all()
            )

    def __load_travel_time_between_locations(self) -> None:
        self.__travel_times_matrix = {}
        self.__travel_times_matrix[0] = {}
        self.__travel_times_matrix[0][0] = 0

        for i, scheduling in enumerate(self.__schedulings):
            self.__travel_times_matrix[0][i] = (
                self.__google_maps_client.get_travel_time_between(
                    self.departure_coordinates, scheduling.location.coordinates
                )
            )
            self.__travel_times_matrix[i] = {}
            self.__travel_times_matrix[i][i] = 0

            for j, other_scheduling in enumerate(self.__schedulings):
                if i != j:
                    self.__travel_times_matrix[i][j] = (
                        self.__google_maps_client.get_travel_time_between(
                            scheduling.location.coordinates,
                            other_scheduling.location.coordinates,
                        )
                    )

    def __clusterize_schedulings_by_space_and_time(self) -> None:
        normalized_schedulings = self.__normalize_schedulings()
        dbscan_scheduling_clusters = self.__clusterize_schedulings_with_dbscan(
            normalized_schedulings
        )
        scheduling_clusters = self.__split_sensitive_patient_clusters(
            dbscan_scheduling_clusters
        )
        self.__schedulings_clusters = scheduling_clusters

    def __normalize_schedulings(self) -> List[List[float]]:
        normalized_schedulings = []
        for scheduling in self.__schedulings:
            normalized_latitude = (
                scheduling.location.coordinates.latitude
                - self.__departure_coordinates.latitude
            ) * 10
            normalized_logitude = (
                scheduling.location.coordinates.longitude
                - self.__departure_coordinates.longitude
            ) * 10
            normalized_datetime_in_minutes = (
                scheduling.datetime.hour * 60 + scheduling.datetime.minute
            ) / 30

            normalized_schedulings.append(
                [
                    normalized_latitude,
                    normalized_logitude,
                    normalized_datetime_in_minutes,
                ]
            )

        return numpy.array(normalized_schedulings)

    def __clusterize_schedulings_with_dbscan(
        self, normalized_schedulings: List[List[float]]
    ) -> Dict[int, List[Scheduling]]:
        dbscan = DBSCAN(
            eps=self.__dbscan_epsilon, min_samples=self.__dbscan_min_samples
        )

        scheduling_clusters: Dict[int, List[Scheduling]] = {}
        for i, cluster_id in enumerate(dbscan.fit_predict(normalized_schedulings)):
            if cluster_id not in scheduling_clusters:
                scheduling_clusters[cluster_id] = []
            scheduling_clusters[cluster_id].append(self.__schedulings[i])
        return scheduling_clusters

    def __split_sensitive_patient_clusters(
        self, scheduling_clusters: Dict[int, List[Scheduling]]
    ) -> List[List[Scheduling]]:
        final_scheduling_clusters = []
        for schedulings in scheduling_clusters.values():
            sensitive_schedulings = [s for s in schedulings if s.sensitive_patient]
            normal_schedulings = [s for s in schedulings if not s.sensitive_patient]

            for scheduling in sensitive_schedulings:
                final_scheduling_clusters.append([scheduling])

            if normal_schedulings:
                final_scheduling_clusters.append(normal_schedulings)
        return final_scheduling_clusters

    def __run_vrptw_for_cluster(self, cluster: List[Scheduling]) -> None:
        schedulings_indexes = []
        for scheduling in cluster:
            schedulings_indexes.append(self.__schedulings.index(scheduling) + 1)

        destination_count = len(schedulings_indexes) + 1

        departure_and_schedulings_indexes = [0] + schedulings_indexes
        travel_time_submatrix = numpy.zeros((destination_count, destination_count))
        for i in range(destination_count):
            for j in range(destination_count):
                travel_time_submatrix[i, j] = self.__travel_times_matrix[
                    departure_and_schedulings_indexes[i],
                    departure_and_schedulings_indexes[j],
                ]

        vehicles_count = min(len(cluster), len(self.__vehicles_relation))
        manager = pywrapcp.RoutingIndexManager(destination_count, vehicles_count, 0)
        routing = pywrapcp.RoutingModel(manager)

        def time_callback(from_index, to_index):
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return int(travel_time_submatrix[from_node, to_node])

        transit_callback_index = routing.RegisterTransitCallback(time_callback)
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        def demand_callback(from_index):
            from_node = manager.IndexToNode(from_index)
            if from_node == 0:
                return 0
            scheduling_idx = schedulings_indexes[from_node - 1]
            return self.__schedulings[scheduling_idx].get_passenger_count()

        demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
        routing.AddDimensionWithVehicleCapacity(
            demand_callback_index,
            0,
            [v.capacity for v in self.__vehicles_relation[:vehicles_count]],
            True,
            "Vehicle Capacity",
        )

        time_dimension_name = "Time"
        routing.AddDimension(
            transit_callback_index,
            60 * 60,  # permite espera de até 1 hora
            24 * 60 * 60,
            False,
            time_dimension_name,
        )
        time_dimension = routing.GetDimensionOrDie(time_dimension_name)

        for i, scheduling_idx in enumerate(schedulings_indexes):
            index = manager.NodeToIndex(i + 1)
            scheduling: Scheduling = self.__schedulings[scheduling_idx - 1]

            scheduling_time_seconds = (
                scheduling.datetime.hour * 3600 + scheduling.datetime.minute * 60
            )

            latest_arrival = scheduling_time_seconds - 15 * 60  # 15 min minutos antes
            earliest_arrival = (
                scheduling_time_seconds - 2 * 60 * 60
            )  # 2 max horas antes
            earliest_arrival = max(0, earliest_arrival)

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
            raise Exception("No solution found")

        roadmaps: List[Roadmap] = []
        for vehicle_id in range(vehicles_count):
            index = routing.Start(vehicle_id)
            if not routing.IsEnd(solution.Value(routing.NextVar(index))):
                roadmap_schedulings: List[Scheduling] = []
                passanger_count = 0

                while not routing.IsEnd(index):
                    node_index = manager.IndexToNode(index)
                    if node_index > 0:
                        scheduling_idx = schedulings_indexes[node_index - 1]
                        scheduling = self.__schedulings[scheduling_idx - 1]
                        roadmap_schedulings.append(scheduling)
                        passanger_count += scheduling.get_passenger_count()
                    index = solution.Value(routing.NextVar(index))

                if roadmap_schedulings:
                    first_scheduling: Scheduling = min(
                        roadmap_schedulings, key=lambda p: p.datetime
                    )
                    first_scheduling_travel_time = self.__travel_times_matrix[
                        0, self.__schedulings.index(first_scheduling) + 1
                    ]

                    if len(roadmap_schedulings) > 1:
                        first_scheduling_travel_time += (
                            (len(roadmap_schedulings) - 1) * 15 * 60
                        )  # 15 minutos por parada adicional

                    departure_time = first_scheduling.datetime - relativedelta(
                        seconds=int(first_scheduling_travel_time + 30 * 60)
                    )  # 30 min de margem

                    last_scheduling: Scheduling = max(
                        roadmap_schedulings, key=lambda p: p.datetime
                    )
                    last_scheduling_travel_time = self.__travel_times_matrix[
                        self.__schedulings.index(last_scheduling) + 1, 0
                    ]

                    arrival_time = last_scheduling.datetime + relativedelta(
                        hours=last_scheduling.average_duration.hour,
                        minutes=last_scheduling.average_duration.minute,
                        seconds=int(last_scheduling_travel_time),
                    )

                    vehicle = self.__vehicles_relation[vehicle_id]
                    driver_id = None
                    if vehicle.default_driver_id:
                        driver_id = vehicle.default_driver_id
                    roadmap = Roadmap(
                        driver_id=driver_id,
                        vehicle_id=vehicle.id,
                        departure=datetime(
                            year=self.__date.year,
                            month=self.__date.month,
                            day=self.__date.day,
                            hour=departure_time.hour,
                            minute=departure_time.minute,
                            second=departure_time.second,
                        ),
                        arrival=datetime(
                            year=self.__date.year,
                            month=self.__date.month,
                            day=self.__date.day,
                            hour=arrival_time.hour,
                            minute=arrival_time.minute,
                            second=arrival_time.second,
                        ),
                    )
                    roadmap.schedulings = roadmap_schedulings
                    roadmaps.append(roadmap)

        return roadmaps

    def __assign_drivers_to_roadmaps_without_it(
        self, roadmaps: List[Roadmap]
    ) -> List[Roadmap]:
        available_drivers = []
        on_call_drivers = []

        for driver in self.__drivers_relation:
            if driver.id in self.__on_call_driver_ids:
                on_call_drivers.append(driver)
            else:
                available_drivers.append(driver)

        prioritized_drivers = available_drivers + on_call_drivers

        driver_schedules = {driver.id: [] for driver in prioritized_drivers}

        for roadmap in roadmaps:
            if roadmap.driver_id:
                driver_schedules[roadmap.driver_id].append(
                    {"start": roadmap.departure, "end": roadmap.arrival}
                )

        def is_driver_available(
            roadmap: Roadmap, driver_occupied_times: List[Dict]
        ) -> bool:
            roadmap_start = roadmap.departure
            roadmap_end = roadmap.arrival

            for occupied_time in driver_occupied_times:
                occupied_start = occupied_time["start"]
                occupied_end = occupied_time["end"]

                if not (roadmap_end <= occupied_start or roadmap_start >= occupied_end):
                    return False

            return True

        for roadmap in roadmaps:
            if roadmap.driver_id:
                continue

            assigned_driver = None
            for driver in prioritized_drivers:
                if is_driver_available(roadmap, driver_schedules[driver.id]):
                    assigned_driver = driver
                    break

            if assigned_driver:
                roadmap.driver_id = assigned_driver.id
                driver_schedules[assigned_driver.id].append(
                    {"start": roadmap.departure, "end": roadmap.arrival}
                )

        return roadmaps
