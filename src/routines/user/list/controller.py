from typing import Any, List, Type

from common.controller.base_entity_controller import ModelType
from common.controller.base_list_controller import BaseListController
from routines.user.add.controller import UserAddController
from routines.user.change.controller import UserChangeController
from routines.user.list.widget import UserListWidget
from routines.user.model import User
from routines.user.remove.controller import UserRemoveController


class UserListController(BaseListController[User]):
    _widget: UserListWidget

    def _get_widget_instance(self) -> UserListWidget:
        return UserListWidget()

    def _get_model_class(self) -> Type[ModelType]:
        return User

    def _build_list_filters(self) -> List[Any]:
        filters = []
        if self._widget.name_filter.text():
            filters.append(User.name.ilike(f"%{self._widget.name_filter.text()}%"))
        return filters

    def _set_widget_connections(self) -> None:
        super()._set_widget_connections()
        self._widget.add_button.clicked.connect(self.__add_button_clicked)
        self._widget.change_button.clicked.connect(self.__change_button_clicked)
        self._widget.remove_button.clicked.connect(self.__remove_button_clicked)
 
    def __add_button_clicked(self) -> None:
        self.add_controller = UserAddController(self)
        self.add_controller.show()

    def __change_button_clicked(self) -> None:
        self.change_controller = UserChangeController(self._selected_model, self)
        self.change_controller.show()

    def __remove_button_clicked(self) -> None:
        self.remove_controller = UserRemoveController(self._selected_model, self)
        self.remove_controller.show()
