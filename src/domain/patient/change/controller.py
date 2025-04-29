from typing import Any, Dict, Optional, Type

from common.controller.base_change_controller import BaseChangeController
from common.controller.base_entity_controller import ModelType
from common.gui.widget.base_change_widget import BaseChangeWidget
from domain.patient.change.widget import PatientChangeWidget
from domain.patient.model import Patient


class PatientChangeController(BaseChangeController[Patient]):
    _widget: PatientChangeWidget

    def _populate_form(self, entity: Patient) -> None:
        self._widget.name_field.setText(entity.name)
        self._widget.cpf_field.setText(entity.format_cpf())
        self._widget.phone_field.setText(entity.format_phone())

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
            self._widget.show_info_pop_up("Atenção", "O CPF é inválido")
            return None

        phone = self._widget.phone_field.get_phone_number()
        if phone and not self._widget.phone_field.is_valid_phone():
            self._widget.show_info_pop_up("Atenção", "O telefone é inválido")
            return None
        
        return {
            "name": name.strip(),
            "cpf": cpf,
            "phone": phone,
        }

    def _get_widget_instance(self) -> BaseChangeWidget:
        return PatientChangeWidget()

    def _get_model_class(self) -> Type[ModelType]:
        return Patient
