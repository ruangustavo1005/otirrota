from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QCloseEvent, QIcon
from PySide6.QtWidgets import QApplication, QLabel, QMenuBar, QVBoxLayout

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
        self.vehicle_menu_item = QAction(
            text="Veículos", icon=QIcon(Settings.FAV_ICON_FILE_NAME), parent=self
        )
        self.patient_menu_item = QAction(
            text="Pacientes", icon=QIcon(Settings.FAV_ICON_FILE_NAME), parent=self
        )
        self.location_menu_item = QAction(
            text="Locais", icon=QIcon(Settings.FAV_ICON_FILE_NAME), parent=self
        )
        self.scheduling_menu_item = QAction(
            text="Agendamentos", icon=QIcon(Settings.FAV_ICON_FILE_NAME), parent=self
        )
        self.roadmap_menu_item = QAction(
            text="Rotas", icon=QIcon(Settings.FAV_ICON_FILE_NAME), parent=self
        )
        self.routes_menu.addActions(
            [
                self.purpose_menu_item,
                self.user_menu_item,
                self.driver_menu_item,
                self.vehicle_menu_item,
                self.patient_menu_item,
                self.location_menu_item,
                self.scheduling_menu_item,
                self.roadmap_menu_item,
            ]
        )

    def __create_logged_user_label(self):
        self.logged_user_label = QLabel("")
        self.logged_user_label.setAlignment(
            Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight
        )
        self.base_layout.addWidget(self.logged_user_label)

    def closeEvent(self, event: QCloseEvent) -> None:
        QApplication.quit()
