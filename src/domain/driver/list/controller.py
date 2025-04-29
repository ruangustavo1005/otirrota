from typing import Any, List, Type

from common.controller.base_entity_controller import ModelType
from common.controller.base_list_controller import BaseListController
from domain.driver.add.controller import DriverAddController
from domain.driver.change.controller import DriverChangeController
from domain.driver.list.widget import DriverListWidget
from domain.driver.model import Driver
from domain.driver.remove.controller import DriverRemoveController


class DriverListController(BaseListController[Driver]):
    _widget: DriverListWidget

    def _get_widget_instance(self) -> DriverListWidget:
        return DriverListWidget()

    def _get_model_class(self) -> Type[ModelType]:
        return Driver

    def _build_list_filters(self) -> List[Any]:
        filters = []
        if self._widget.name_filter.text():
            filters.append(Driver.name.ilike(f"%{self._widget.name_filter.text()}%"))
        if self._widget.cpf_filter.get_cpf_numbers():
            filters.append(
                Driver.cpf.ilike(f"%{self._widget.cpf_filter.get_cpf_numbers()}%")
            )
        if self._widget.registration_number_filter.text():
            filters.append(
                Driver.registration_number.ilike(
                    f"%{self._widget.registration_number_filter.text()}%"
                )
            )
        filters.append(Driver.active == self._widget.active_filter.isChecked())
        return filters

    def _set_widget_connections(self) -> None:
        super()._set_widget_connections()
        self._widget.add_button.clicked.connect(self.__add_button_clicked)
        self._widget.change_button.clicked.connect(self.__change_button_clicked)
        self._widget.remove_button.clicked.connect(self.__remove_button_clicked)

    def __add_button_clicked(self) -> None:
        self.add_controller = DriverAddController(self)
        self.add_controller.show()

    def __change_button_clicked(self) -> None:
        self.change_controller = DriverChangeController(self._selected_model, self)
        self.change_controller.show()

    def __remove_button_clicked(self) -> None:
        self.remove_controller = DriverRemoveController(self._selected_model, self)
        self.remove_controller.show()
