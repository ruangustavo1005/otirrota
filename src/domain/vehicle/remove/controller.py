from typing import Type

from common.controller.base_entity_controller import ModelType
from common.controller.base_remove_controller import BaseRemoveController
from domain.vehicle.model import Vehicle


class VehicleRemoveController(BaseRemoveController[Vehicle]):
    def _get_model_class(self) -> Type[ModelType]:
        return Vehicle
