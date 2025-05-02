from typing import Any, List, Type

from PySide6.QtGui import QDesktopServices
from PySide6.QtCore import QUrl

from common.controller.base_entity_controller import ModelType
from common.controller.base_list_controller import BaseListController
from domain.location.add.controller import LocationAddController

from domain.location.change.controller import LocationChangeController
from domain.location.list.widget import LocationListWidget
from domain.location.model import Location
from domain.location.remove.controller import LocationRemoveController


class LocationListController(BaseListController[Location]):
    _widget: LocationListWidget

    def _get_widget_instance(self) -> LocationListWidget:
        return LocationListWidget()

    def _get_model_class(self) -> Type[ModelType]:
        return Location

    def _build_list_filters(self) -> List[Any]:
        filters = []
        if self._widget.descricao_filter.text():
            filters.append(
                Location.description.ilike(f"%{self._widget.descricao_filter.text()}%")
            )
        return filters

    def _set_widget_connections(self) -> None:
        super()._set_widget_connections()
        self._widget.add_button.clicked.connect(self.__add_button_clicked)
        self._widget.change_button.clicked.connect(self.__change_button_clicked)
        self._widget.remove_button.clicked.connect(self.__remove_button_clicked)
        self._widget.open_maps_button.clicked.connect(self.__open_maps_button_clicked)

    def __add_button_clicked(self) -> None:
        self.add_controller = LocationAddController(self)
        self.add_controller.show()

    def __change_button_clicked(self) -> None:
        self.change_controller = LocationChangeController(self._selected_model, self)
        self.change_controller.show()

    def __remove_button_clicked(self) -> None:
        self.remove_controller = LocationRemoveController(self._selected_model, self)
        self.remove_controller.show()

    def __open_maps_button_clicked(self) -> None:
        url = f"https://www.google.com/maps/@{self._selected_model.coordinates.latitude},{self._selected_model.coordinates.longitude},15z"
        QDesktopServices.openUrl(QUrl(url))
