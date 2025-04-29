from typing import Type

from common.controller.base_entity_controller import ModelType
from common.controller.base_remove_controller import BaseRemoveController
from domain.patient.model import Patient


class PatientRemoveController(BaseRemoveController[Patient]):
    def _get_model_class(self) -> Type[ModelType]:
        return Patient
