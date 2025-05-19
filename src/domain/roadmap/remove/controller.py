from datetime import date
from typing import Type

from common.controller.base_entity_controller import ModelType
from common.controller.base_remove_controller import BaseRemoveController
from common.gui.widget.base_widget import BaseWidget
from domain.roadmap.model import Roadmap


class RoadmapRemoveController(BaseRemoveController[Roadmap]):
    def _get_model_class(self) -> Type[ModelType]:
        return Roadmap

    def _remove(self) -> bool:
        if self._entity.departure.date() < date.today():
            BaseWidget.show_warning_pop_up(
                "Atenção",
                "Não é possível excluir um Roteiro que já ocorreu",
            )
            return False
        return super()._remove()
