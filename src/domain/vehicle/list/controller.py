from typing import Any, List, Type

from common.controller.base_entity_controller import ModelType
from common.controller.base_list_controller import BaseListController
from domain.vehicle.add.controller import VehicleAddController
from domain.vehicle.change.controller import VehicleChangeController
from domain.vehicle.list.widget import VehicleListWidget
from domain.vehicle.model import Vehicle
from domain.vehicle.remove.controller import VehicleRemoveController


class VehicleListController(BaseListController[Vehicle]):
    _widget: VehicleListWidget

    def _get_widget_instance(self) -> VehicleListWidget:
        return VehicleListWidget()

    def _get_model_class(self) -> Type[ModelType]:
        return Vehicle

    def _build_list_filters(self) -> List[Any]:
        filters = []

        if self._widget.license_plate_filter.get_license_plate_alphanumeric():
            filters.append(
                Vehicle.license_plate.ilike(
                    f"%{self._widget.license_plate_filter.get_license_plate_alphanumeric()}%"
                )
            )

        if self._widget.description_filter.text():
            filters.append(
                Vehicle.description.ilike(f"%{self._widget.description_filter.text()}%")
            )

        active_filter = self._widget.active_filter.get_current_data()
        if active_filter is not None:
            filters.append(Vehicle.active == active_filter)
        return filters

    def _set_widget_connections(self) -> None:
        super()._set_widget_connections()
        self._widget.add_button.clicked.connect(self.__add_button_clicked)
        self._widget.change_button.clicked.connect(self.__change_button_clicked)
        self._widget.remove_button.clicked.connect(self.__remove_button_clicked)

    def __add_button_clicked(self) -> None:
        self.add_controller = VehicleAddController(self)
        self.add_controller.show()

    def __change_button_clicked(self) -> None:
        self.change_controller = VehicleChangeController(self._selected_model, self)
        self.change_controller.show()

    def __remove_button_clicked(self) -> None:
        self.remove_controller = VehicleRemoveController(self._selected_model, self)
        self.remove_controller.show()
