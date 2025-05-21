from typing import Type
from common.controller.base_crud_controller import BaseCRUDController
from common.controller.base_entity_controller import ModelType
from common.controller.base_list_controller import BaseListController
from common.gui.widget.base_crud_widget import BaseCRUDWidget
from db import Database
from domain.driver.model import Driver
from domain.roadmap.model import Roadmap
from domain.roadmap.suggest.drivers_vehicles_relation.model import (
    DriversVehiclesRelation,
)
from domain.roadmap.suggest.drivers_vehicles_relation.widget import (
    DriversVehiclesRelationWidget,
)
from domain.vehicle.model import Vehicle


class DriversVehiclesRelationController(BaseCRUDController[Roadmap]):
    _widget: DriversVehiclesRelationWidget

    def __init__(self, caller: BaseListController | None = None) -> None:
        super().__init__(caller)

    def execute_action(self) -> None:
        if self._is_relation_valid():
            # TODO: chamar a geração dos roteiros
            pass

    def _is_relation_valid(self) -> bool:
        return True

    def show(self) -> None:
        self._suggest_relations()
        return super().show()

    def _suggest_relations(self) -> None:
        with Database.session_scope(end_with_commit=False) as session:
            drivers = (
                session.query(Driver)
                .join(Vehicle, Vehicle.default_driver_id == Driver.id)
                .filter(Driver.active == True)  # noqa: E712
                .filter(Vehicle.active == True)  # noqa: E712
                .all()
            )
            for driver in drivers:
                self._widget.relations_area.add_relation_row(
                    DriversVehiclesRelation(
                        driver=driver,
                        vehicle=driver.default_from_vehicle,
                        on_call_driver=False,
                    )
                )

    def _get_widget_instance(self) -> BaseCRUDWidget:
        return DriversVehiclesRelationWidget()

    def _get_model_class(self) -> Type[ModelType]:
        return Roadmap
