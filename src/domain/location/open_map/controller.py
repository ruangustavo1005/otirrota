from typing import Type

from common.controller.base_entity_controller import ModelType
from common.controller.base_remove_controller import BaseRemoveController
from domain.location.model import Location


class LocationRemoveController(BaseRemoveController[Location]):
    def _get_model_class(self) -> Type[ModelType]:
        return Location
