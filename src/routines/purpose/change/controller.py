from typing import Any, Dict, Optional, Type

from common.controller.base_change_controller import BaseChangeController
from common.controller.base_controller import ModelType
from common.gui.widget.base_change_widget import BaseChangeWidget
from routines.purpose.change.widget import PurposeChangeWidget
from routines.purpose.model import Purpose


class PurposeChangeController(BaseChangeController[Purpose]):
    _widget: PurposeChangeWidget

    def _populate_form(self, entity: Purpose) -> None:
        self._widget.description_field.setText(entity.description)

    def _get_model_updates(self) -> Optional[Dict[str, Any]]:
        description = self._widget.description_field.text()
        if not description:
            self._widget.show_info_pop_up("Atenção", "A descrição é obrigatória")
            return None
        return {
            "description": description.strip(),
        }

    def _get_widget_instance(self) -> BaseChangeWidget:
        return PurposeChangeWidget()

    def _get_model_class(self) -> Type[ModelType]:
        return Purpose
