from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QLabel, QMenuBar, QVBoxLayout

from common.gui.widget.base_widget import BaseWidget
from settings import Settings


class MenuWidget(BaseWidget):
    def __init__(self, parent=None, flags=Qt.WindowFlags()):
        super().__init__("Menu", 800, 600, parent, flags)

    def _init_ui(self) -> None:
        self.base_layout = QVBoxLayout()
        self.__create_menu()
        self.__create_logged_user_label()
        self.setLayout(self.base_layout)

    def __create_menu(self):
        self.menu_bar = QMenuBar()
        self.__create_management_menu()
        self.base_layout.setMenuBar(self.menu_bar)

    def __create_management_menu(self):
        self.routes_menu = self.menu_bar.addMenu("Gerenciamento")
        self.purpose_menu_item = QAction(
            text="Finalidades", icon=QIcon(Settings.FAV_ICON_FILE_NAME), parent=self
        )
        self.user_menu_item = QAction(
            text="Usuários", icon=QIcon(Settings.FAV_ICON_FILE_NAME), parent=self
        )
        self.driver_menu_item = QAction(
            text="Motoristas", icon=QIcon(Settings.FAV_ICON_FILE_NAME), parent=self
        )
        self.routes_menu.addActions(
            [
                self.purpose_menu_item,
                self.user_menu_item,
                self.driver_menu_item,
            ]
        )

    def __create_logged_user_label(self):
        self.logged_user_label = QLabel("")
        self.logged_user_label.setAlignment(
            Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight
        )
        self.base_layout.addWidget(self.logged_user_label)
