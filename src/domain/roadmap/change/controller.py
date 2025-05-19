from datetime import datetime
from typing import Optional, Type

from PySide6.QtCore import QDate, QTime
from PySide6.QtWidgets import QTableWidgetItem
from sqlalchemy.orm import Session

from common.controller.base_change_controller import BaseChangeController
from common.controller.base_entity_controller import ModelType
from common.gui.widget.base_change_widget import BaseChangeWidget
from db import Database
from domain.roadmap.change.widget import RoadmapChangeWidget
from domain.roadmap.model import Roadmap
from domain.scheduling.model import Scheduling
from domain.scheduling.view.controller import SchedulingViewController
from settings import Settings


class RoadmapChangeController(BaseChangeController[Roadmap]):
    _widget: RoadmapChangeWidget

    def _populate_form(self, entity: Roadmap) -> None:
        self._widget.date_field.setDate(
            QDate(
                entity.departure.year,
                entity.departure.month,
                entity.departure.day,
            )
        )
        self._widget.driver_combo_box.setCurrentIndexByData(entity.driver)
        self._widget.vehicle_combo_box.setCurrentIndexByData(entity.vehicle)
        for scheduling in entity.schedulings:
            row_count = self._widget.schedulings_table.rowCount()
            self._widget.schedulings_table.insertRow(row_count)
            self._widget.schedulings_table.setItem(
                row_count, 0, QTableWidgetItem(str(scheduling.id))
            )
            self._widget.schedulings_table.setItem(
                row_count, 1, QTableWidgetItem(scheduling.get_description())
            )
        self._widget.departure_time_field.setTime(
            QTime(
                entity.departure.hour,
                entity.departure.minute,
            )
        )
        self._widget.arrival_time_field.setTime(
            QTime(
                entity.arrival.hour,
                entity.arrival.minute,
            )
        )

    def _get_model_updates(self) -> Optional[Roadmap]:
        driver = self._widget.driver_combo_box.get_current_data()
        if not driver:
            self._widget.show_info_pop_up("Atenção", "Selecione um motorista")
            return None
        if not driver.active:
            self._widget.show_info_pop_up(
                "Atenção", "O motorista selecionado não está ativo"
            )
            return None

        vehicle = self._widget.vehicle_combo_box.get_current_data()
        if not vehicle:
            self._widget.show_info_pop_up("Atenção", "Selecione um veículo")
            return None
        if not vehicle.active:
            self._widget.show_info_pop_up(
                "Atenção", "O veículo selecionado não está ativo"
            )
            return None

        departure_time = self._widget.departure_time_field.time().toPython()
        arrival_time = self._widget.arrival_time_field.time().toPython()
        if departure_time >= arrival_time:
            self._widget.show_info_pop_up(
                "Atenção", "A hora de partida tem que ser menor que a hora de chegada"
            )
            return None

        date = self._widget.date_field.date().toPython()
        return {
            "driver_id": driver.id,
            "vehicle_id": vehicle.id,
            "departure": datetime.combine(date, departure_time),
            "arrival": datetime.combine(date, arrival_time),
            "creation_user_id": Settings.get_logged_user().id,
        }

    def _change(self) -> bool:
        with Database.session_scope() as session:
            try:
                if updates := self._get_model_updates():
                    entity = self._model_class.get_by_id(
                        self._entity_id, session=session
                    )
                    entity.update(session=session, **updates)
                    self.update_schedulings(entity, session)
                    self._widget.show_info_pop_up(
                        "Sucesso",
                        f"{self._model_class.get_static_description()} alterado(a) com sucesso",
                    )
                    self._widget.close()
                    return True
            except ValueError as e:
                self._widget.show_info_pop_up("Atenção", str(e))
                session.rollback()
                return False
            except Exception as e:
                self._handle_change_exception(e)
                return False

    def update_schedulings(self, roadmap: Roadmap, session: Session) -> None:
        scheduling_ids = self._widget._get_scheduling_ids_from_table()

        if not scheduling_ids:
            raise ValueError("Adicione pelo menos um agendamento")

        total_passangers = 0
        schedulings = (
            session.query(Scheduling).filter(Scheduling.id.in_(scheduling_ids)).all()
        )
        for scheduling in schedulings:
            total_passangers += scheduling.get_passenger_count()

        if total_passangers > roadmap.vehicle.capacity:
            raise ValueError(
                f"O veículo não tem capacidade para transportar todos {total_passangers} passageiros"
            )

        removed_schedulings = (
            session.query(Scheduling)
            .filter(
                Scheduling.roadmap_id == roadmap.id,
                Scheduling.id.notin_(scheduling_ids),
            )
            .all()
        )
        existent_scheduling_ids = []
        for scheduling in removed_schedulings:
            scheduling.roadmap_id = None
            scheduling.save(session)
            existent_scheduling_ids.append(scheduling.id)

        for scheduling in schedulings:
            if scheduling.id not in existent_scheduling_ids:
                scheduling.roadmap_id = roadmap.id
                scheduling.save(session)

    def _get_widget_instance(self) -> BaseChangeWidget:
        return RoadmapChangeWidget(roadmap_id=self._entity_id)

    def _get_model_class(self) -> Type[ModelType]:
        return Roadmap

    def show(self) -> None:
        self._widget._view_scheduling_button.clicked.connect(
            self._on_view_scheduling_clicked
        )
        self._widget.calculate_departure_arrival_button.clicked.connect(
            self._on_calculate_departure_arrival_clicked
        )
        self._widget.scheduling_combo_box.fill(
            date=self._widget.date_field.date().toPython(),
            ids_ignore=self._widget._get_scheduling_ids_from_table(),
        )
        super().show()

    def _on_view_scheduling_clicked(self) -> None:
        self._scheduling_view_controller = SchedulingViewController(
            self._widget.scheduling_combo_box.get_current_data()
        )
        self._scheduling_view_controller.show()

    def _on_calculate_departure_arrival_clicked(self) -> None:
        pass
