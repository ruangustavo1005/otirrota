from datetime import datetime
from typing import Optional, Type

from PySide6.QtCore import Qt
from sqlalchemy.orm import Session

from common.controller.base_add_controller import BaseAddController
from common.controller.base_entity_controller import ModelType
from common.gui.widget.base_add_widget import BaseAddWidget
from db import Database
from domain.roadmap.add.widget import RoadmapAddWidget
from domain.roadmap.model import Roadmap
from domain.scheduling.model import Scheduling
from settings import Settings


class RoadmapAddController(BaseAddController[Roadmap]):
    _widget: RoadmapAddWidget

    def __init__(self, parent=None):
        super().__init__(parent)

    def _get_populated_model(self) -> Optional[Roadmap]:
        driver = self._widget.driver_combo_box.get_current_data()
        if not driver:
            self._widget.show_info_pop_up("Atenção", "Selecione um motorista")
            return None

        vehicle = self._widget.vehicle_combo_box.get_current_data()
        if not vehicle:
            self._widget.show_info_pop_up("Atenção", "Selecione um veículo")
            return None

        date = self._widget.date_field.dateTime().toPython()
        if date <= datetime.now().date():
            self._widget.show_info_pop_up(
                "Atenção", "A data tem que ser maior que a hoje"
            )
            return None

        departure_time = self._widget.departure_time_field.time()
        arrival_time = self._widget.arrival_time_field.time()
        if departure_time >= arrival_time:
            self._widget.show_info_pop_up(
                "Atenção", "A hora de partida tem que ser menor que a hora de chegada"
            )
            return None

        return Roadmap(
            driver_id=driver.id,
            vehicle_id=vehicle.id,
            departure=datetime.combine(date, departure_time),
            arrival=datetime.combine(date, arrival_time),
            creation_user_id=Settings.get_logged_user().id,
        )

    def _save(self) -> bool:
        with Database.session_scope() as session:
            try:
                if model := self._get_populated_model():
                    model.save(session)
                    session.flush()
                    self.save_schedulings(model, session)
                    self._widget.show_info_pop_up(
                        "Sucesso",
                        f"{self._model_class.get_static_description()} criado(a) com sucesso",
                    )
                    self._widget.close()
                    return True
            except ValueError as e:
                self._widget.show_info_pop_up("Atenção", str(e))
                session.rollback()
                return False
            except Exception as e:
                self._handle_add_exception(e)
                session.rollback()
                return False

    def save_schedulings(self, roadmap: Roadmap, session: Session) -> None:
        scheduling_ids = []
        for row in range(self._widget.schedulings_table.rowCount()):
            scheduling_id = self._widget.schedulings_table.item(row, 0).data(
                Qt.DisplayRole
            )
            if scheduling_id:
                scheduling_ids.append(int(scheduling_id))

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

        for scheduling in schedulings:
            scheduling.roadmap_id = roadmap.id
            scheduling.save(session)

    def _get_widget_instance(self) -> BaseAddWidget:
        return RoadmapAddWidget()

    def _get_model_class(self) -> Type[ModelType]:
        return Roadmap

    def show(self) -> None:
        self._widget.calculate_departure_arrival_button.clicked.connect(
            self._on_calculate_departure_arrival_clicked
        )
        super().show()

    def _on_calculate_departure_arrival_clicked(self) -> None:
        pass
