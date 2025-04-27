import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from db import Database
from routines.menu.controller import MenuController
from routines.user.login.controller import LoginController
from settings import Settings


Database.initialize(
    db_user=Settings.DB_USER,
    db_password=Settings.DB_PASSWORD,
    db_host=Settings.DB_HOST,
    db_port=Settings.DB_PORT,
    db_name=Settings.DB_NAME,
)

app = QApplication(sys.argv)
app.setWindowIcon(QIcon(Settings.FAV_ICON_FILE_NAME))

menu_controller = MenuController()
login_controller = LoginController(menu_controller)

login_controller.show()

sys.exit(app.exec())
