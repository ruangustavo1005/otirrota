from common.controller.base_controller import BaseController
from routines.driver.list.controller import DriverListController
from routines.menu.widget import MenuWidget
from routines.purpose.list.controller import PurposeListController
from routines.user.list.controller import UserListController
from settings import Settings


class MenuController(BaseController):
    _widget: MenuWidget

    def __init__(self):
        super().__init__()
        self.__set_menu_connections()

    def _get_widget_instance(self) -> MenuWidget:
        return MenuWidget()

    def __set_menu_connections(self) -> None:
        self._widget.purpose_menu_item.triggered.connect(
            self.__purpose_menu_item_triggered
        )
        self._widget.user_menu_item.triggered.connect(self.__user_menu_item_triggered)
        self._widget.driver_menu_item.triggered.connect(
            self.__driver_menu_item_triggered
        )

    def __purpose_menu_item_triggered(self) -> None:
        self.purpose_list_controller = PurposeListController()
        self.purpose_list_controller.show()

    def __user_menu_item_triggered(self) -> None:
        self.user_list_controller = UserListController()
        self.user_list_controller.show()

    def __driver_menu_item_triggered(self) -> None:
        self.driver_list_controller = DriverListController()
        self.driver_list_controller.show()

    def show(self) -> None:
        self._widget.logged_user_label.setText(
            f"Bem vindo(a), {Settings.get_logged_user().name}!"
        )
        return super().show()
