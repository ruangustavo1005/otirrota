from typing import Type

from common.controller.base_entity_controller import ModelType
from common.controller.base_remove_controller import BaseRemoveController
from domain.roadmap.model import Roadmap


class RoadmapRemoveController(BaseRemoveController[Roadmap]):
    def _get_model_class(self) -> Type[ModelType]:
        return Roadmap
