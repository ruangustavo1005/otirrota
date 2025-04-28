from typing import Any, List, Type

from common.controller.base_entity_controller import ModelType
from common.controller.base_list_controller import BaseListController
from domain.purpose.add.controller import PurposeAddController
from domain.purpose.change.controller import PurposeChangeController
from domain.purpose.list.widget import PurposeListWidget
from domain.purpose.model import Purpose
from domain.purpose.remove.controller import PurposeRemoveController


class PurposeListController(BaseListController[Purpose]):
    _widget: PurposeListWidget

    def _get_widget_instance(self) -> PurposeListWidget:
        return PurposeListWidget()

    def _get_model_class(self) -> Type[ModelType]:
        return Purpose

    def _build_list_filters(self) -> List[Any]:
        filters = []
        if self._widget.descricao_filter.text():
            filters.append(
                Purpose.description.ilike(f"%{self._widget.descricao_filter.text()}%")
            )
        return filters

    def _set_widget_connections(self) -> None:
        super()._set_widget_connections()
        self._widget.add_button.clicked.connect(self.__add_button_clicked)
        self._widget.change_button.clicked.connect(self.__change_button_clicked)
        self._widget.remove_button.clicked.connect(self.__remove_button_clicked)

    def __add_button_clicked(self) -> None:
        self.add_controller = PurposeAddController(self)
        self.add_controller.show()

    def __change_button_clicked(self) -> None:
        self.change_controller = PurposeChangeController(self._selected_model, self)
        self.change_controller.show()

    def __remove_button_clicked(self) -> None:
        self.remove_controller = PurposeRemoveController(self._selected_model, self)
        self.remove_controller.show()
