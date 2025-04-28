from typing import Any, Dict, Optional, Type

from common.controller.base_change_controller import BaseChangeController
from common.controller.base_entity_controller import ModelType
from common.gui.widget.base_change_widget import BaseChangeWidget
from routines.driver.change.widget import DriverChangeWidget
from routines.driver.model import Driver


class DriverChangeController(BaseChangeController[Driver]):
    _widget: DriverChangeWidget

    def _populate_form(self, entity: Driver) -> None:
        self._widget.name_field.setText(entity.name)
        self._widget.cpf_field.setText(entity.format_cpf())
        self._widget.registration_number_field.setText(entity.registration_number)
        self._widget.active_field.setChecked(entity.active)

    def _get_model_updates(self) -> Optional[Dict[str, Any]]:
        name = self._widget.name_field.text()
        if not name:
            self._widget.show_info_pop_up("Atenção", "O nome é obrigatório")
            return None

        cpf = self._widget.cpf_field.get_cpf_numbers()
        if not cpf:
            self._widget.show_info_pop_up("Atenção", "O CPF é obrigatório")
            return None

        if not self._widget.cpf_field.is_valid_cpf():
            self._widget.show_info_pop_up("Atenção", "O CPF informado não é válido")
            return None

        registration_number = self._widget.registration_number_field.text()
        if not registration_number:
            self._widget.show_info_pop_up(
                "Atenção", "O número de registro é obrigatório"
            )
            return None

        return {
            "name": name.strip(),
            "cpf": cpf,
            "registration_number": registration_number.strip(),
            "active": self._widget.active_field.isChecked(),
        }

    def _get_widget_instance(self) -> BaseChangeWidget:
        return DriverChangeWidget()

    def _get_model_class(self) -> Type[ModelType]:
        return Driver
