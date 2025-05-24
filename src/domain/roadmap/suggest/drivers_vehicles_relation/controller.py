from typing import Type

from common.controller.base_crud_controller import BaseCRUDController
from common.controller.base_entity_controller import ModelType
from common.controller.base_list_controller import BaseListController
from common.gui.widget.base_crud_widget import BaseCRUDWidget
from db import Database
from domain.driver.model import Driver
from domain.roadmap.model import Roadmap
from domain.roadmap.suggest.drivers_vehicles_relation.widget import (
    DriversVehiclesRelationWidget,
)
from domain.vehicle.model import Vehicle


class DriversVehiclesRelationController(BaseCRUDController[Roadmap]):
    _widget: DriversVehiclesRelationWidget

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

        # TODO: chamar a geração dos roteiros

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
        return DriversVehiclesRelationWidget()

    def _get_model_class(self) -> Type[ModelType]:
        return Roadmap
