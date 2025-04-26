from typing import Optional, Type
from common.controller.base_add_controller import BaseAddController
from common.controller.base_controller import ModelType
from common.gui.widget.base_add_widget import BaseAddWidget
from routines.purpose.add.widget import PurposeAddWidget
from routines.purpose.model import Purpose


class PurposeAddController(BaseAddController[Purpose]):
    _widget: PurposeAddWidget

    def _get_populated_model(self) -> Optional[Purpose]:
        description = self._widget.description_field.text()
        if not description:
            self._widget.show_info_pop_up("Atenção", "A descrição é obrigatória")
            return None
        return Purpose(description=description.strip())

    def _get_widget_instance(self) -> BaseAddWidget:
        return PurposeAddWidget()

    def _get_model_class(self) -> Type[ModelType]:
        return Purpose
