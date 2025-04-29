from typing import Optional, Type

from common.controller.base_add_controller import BaseAddController
from common.controller.base_entity_controller import ModelType
from common.gui.widget.base_add_widget import BaseAddWidget
from domain.patient.add.widget import PatientAddWidget
from domain.patient.model import Patient


class PatientAddController(BaseAddController[Patient]):
    _widget: PatientAddWidget

    def _get_populated_model(self) -> Optional[Patient]:
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
        return Patient(name=name.strip(), cpf=cpf, phone=phone)

    def _get_widget_instance(self) -> BaseAddWidget:
        return PatientAddWidget()

    def _get_model_class(self) -> Type[ModelType]:
        return Patient
