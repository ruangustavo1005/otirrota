from typing import Type

from common.controller.base_entity_controller import ModelType
from common.controller.base_remove_controller import BaseRemoveController
from routines.driver.model import Driver


class DriverRemoveController(BaseRemoveController[Driver]):
    def _get_model_class(self) -> Type[ModelType]:
        return Driver
