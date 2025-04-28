from typing import Optional, Type

from common.controller.base_add_controller import BaseAddController
from common.controller.base_entity_controller import ModelType
from common.gui.widget.base_add_widget import BaseAddWidget
from domain.driver.add.widget import DriverAddWidget
from domain.driver.model import Driver


class DriverAddController(BaseAddController[Driver]):
    _widget: DriverAddWidget

    def _get_populated_model(self) -> Optional[Driver]:
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

        return Driver(
            name=name.strip(),
            cpf=cpf,
            registration_number=registration_number.strip(),
        )

    def _get_widget_instance(self) -> BaseAddWidget:
        return DriverAddWidget()

    def _get_model_class(self) -> Type[ModelType]:
        return Driver
