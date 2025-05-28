from datetime import datetime
from typing import Optional, Type

from sqlalchemy.orm import Session

from common.controller.base_add_controller import BaseAddController
from common.controller.base_entity_controller import ModelType
from common.gui.widget.base_add_widget import BaseAddWidget
from db import Database
from domain.roadmap.add.widget import RoadmapAddWidget
from domain.roadmap.model import Roadmap
from domain.scheduling.model import Scheduling
from domain.scheduling.view.controller import SchedulingViewController
from settings import Settings


class RoadmapAddController(BaseAddController[Roadmap]):
    _widget: RoadmapAddWidget

    def _get_populated_model(self) -> Optional[Roadmap]:
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

        date = self._widget.date_field.date().toPython()
        if date < datetime.now().date():
            self._widget.show_info_pop_up(
                "Atenção", "A data não pode ser menor que hoje"
            )
            return None

        departure_time = self._widget.departure_time_field.time().toPython()
        arrival_time = self._widget.arrival_time_field.time().toPython()
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

        for scheduling in schedulings:
            scheduling.roadmap_id = roadmap.id
            scheduling.save(session)

    def _get_widget_instance(self) -> BaseAddWidget:
        return RoadmapAddWidget()

    def _get_model_class(self) -> Type[ModelType]:
        return Roadmap

    def show(self) -> None:
        self._widget._view_scheduling_button.clicked.connect(
            self._on_view_scheduling_clicked
        )
        self._widget.scheduling_combo_box.fill(
            date=self._widget.date_field.date().toPython(),
        )
        super().show()

    def _on_view_scheduling_clicked(self) -> None:
        self._scheduling_view_controller = SchedulingViewController(
            self._widget.scheduling_combo_box.get_current_data()
        )
        self._scheduling_view_controller.show()
