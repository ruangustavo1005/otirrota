from typing import Type

from common.controller.base_entity_controller import ModelType
from common.controller.base_remove_controller import BaseRemoveController
from common.gui.widget.base_widget import BaseWidget
from domain.scheduling.model import Scheduling


class SchedulingRemoveController(BaseRemoveController[Scheduling]):
    def _get_model_class(self) -> Type[ModelType]:
        return Scheduling

    def _remove(self) -> bool:
        if self._entity.roadmap:
            BaseWidget.show_warning_pop_up(
                "Atenção",
                f"Não é possível excluir este(a) {self._model_class.get_static_description()}",
                f"Existem registros de {self._entity.roadmap.get_static_description()} vinculados que impedem a exclusão.",
            )
            return False
        return super()._remove()
