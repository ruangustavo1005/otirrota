from typing import Type

from common.controller.base_crud_controller import BaseCRUDController
from common.controller.base_entity_controller import ModelType
from common.controller.base_list_controller import BaseListController
from common.gui.widget.base_crud_widget import BaseCRUDWidget
from db import Database
from domain.config.model import Config
from domain.driver.model import Driver
from domain.roadmap.model import Roadmap
from domain.roadmap.suggest.widget import (
    SuggestRoadmapsWidget,
)
from domain.roadmap.suggest.optimizer import RoadmapOptimizer
from domain.vehicle.model import Vehicle
from settings import Settings


class SuggestRoadmapsController(BaseCRUDController[Roadmap]):
    _widget: SuggestRoadmapsWidget

    def __init__(self, caller: BaseListController | None = None) -> None:
        super().__init__(caller)

    def execute_action(self) -> None:
        vehicles_relation = self._widget.vehicles_relation_group_widget.get_relations()
        if len(vehicles_relation) == 0:
            self._widget.show_warning_pop_up(
                "Atenção",
                "Selecione pelo menos um veículo para gerar os roteiros",
            )
            return

        drivers_relation = self._widget.drivers_relation_group_widget.get_relations()
        if len(drivers_relation) == 0:
            self._widget.show_warning_pop_up(
                "Atenção",
                "Selecione pelo menos um motorista para gerar os roteiros",
            )
            return

        on_call_driver_ids = []
        for i, (driver, on_call) in enumerate(drivers_relation[:]):
            drivers_relation[i] = driver
            if on_call:
                on_call_driver_ids.append(driver.id)

        try:
            config = Config.get_config()
            optimizer = RoadmapOptimizer(
                date=self._widget.date_field.date().toPython(),
                vehicles_relation=vehicles_relation,
                drivers_relation=drivers_relation,
                on_call_driver_ids=on_call_driver_ids,
                departure_coordinates=config.departure_coordinates,
                dbscan_epsilon=config.eplison,
                dbscan_min_samples=config.minpts,
            )

            optimizer.status_updated.connect(self._on_optimizer_status_updated)

            self._widget.show_loading("Iniciando geração de roteiros...")

            optimized_roadmaps = optimizer.generate_roadmaps()

            with Database.session_scope() as session:
                for roadmap in optimized_roadmaps:
                    roadmap.creation_user_id = Settings.get_logged_user().id
                    roadmap.save(session)

            self._widget.hide_loading()
            self._widget.show_info_pop_up("Sucesso", "Roteiros gerados com sucesso")
            if self._caller and hasattr(self._caller, "roadmaps_suggested_for"):
                self._caller.roadmaps_suggested_for(self._widget.date_field.date())
            self._widget.close()

        except Exception as e:
            self._widget.hide_loading()
            self._widget.show_error_pop_up(
                "Erro", "Erro ao gerar os roteiros", f"Detalhes: {str(e)}"
            )
            return

    def _on_optimizer_status_updated(self, message: str):
        self._widget.update_loading_message(message)

    def show(self) -> None:
        self._suggest_relations()
        return super().show()

    def _suggest_relations(self) -> None:
        with Database.session_scope(end_with_commit=False) as session:
            drivers = (
                session.query(Driver).filter(Driver.active == True).all()  # noqa: E712
            )
            for driver in drivers:
                self._widget.drivers_relation_group_widget.add_relation_row(driver)

            vehicles = (
                session.query(Vehicle)
                .filter(Vehicle.active == True)  # noqa: E712
                .all()
            )
            for vehicle in vehicles:
                self._widget.vehicles_relation_group_widget.add_relation_row(vehicle)

    def _get_widget_instance(self) -> BaseCRUDWidget:
        return SuggestRoadmapsWidget()

    def _get_model_class(self) -> Type[ModelType]:
        return Roadmap
