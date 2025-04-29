from typing import Any, List, Type

from common.controller.base_entity_controller import ModelType
from common.controller.base_list_controller import BaseListController
from domain.patient.add.controller import PatientAddController
from domain.patient.change.controller import PatientChangeController
from domain.patient.list.widget import PatientListWidget
from domain.patient.model import Patient
from domain.patient.remove.controller import PatientRemoveController


class PatientListController(BaseListController[Patient]):
    _widget: PatientListWidget

    def _get_widget_instance(self) -> PatientListWidget:
        return PatientListWidget()

    def _get_model_class(self) -> Type[ModelType]:
        return Patient

    def _build_list_filters(self) -> List[Any]:
        filters = []
        if self._widget.nome_filter.text():
            filters.append(Patient.name.ilike(f"%{self._widget.nome_filter.text()}%"))
        if self._widget.cpf_filter.get_cpf_numbers():
            filters.append(
                Patient.cpf.ilike(f"%{self._widget.cpf_filter.get_cpf_numbers()}%")
            )
        return filters

    def _set_widget_connections(self) -> None:
        super()._set_widget_connections()
        self._widget.add_button.clicked.connect(self.__add_button_clicked)
        self._widget.change_button.clicked.connect(self.__change_button_clicked)
        self._widget.remove_button.clicked.connect(self.__remove_button_clicked)

    def __add_button_clicked(self) -> None:
        self.add_controller = PatientAddController(self)
        self.add_controller.show()

    def __change_button_clicked(self) -> None:
        self.change_controller = PatientChangeController(self._selected_model, self)
        self.change_controller.show()

    def __remove_button_clicked(self) -> None:
        self.remove_controller = PatientRemoveController(self._selected_model, self)
        self.remove_controller.show()
