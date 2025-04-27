import sys
from sqlalchemy.exc import OperationalError
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from common.gui.widget.base_widget import BaseWidget
from db import Database
from routines.menu.controller import MenuController
from routines.user.login.controller import LoginController
from settings import Settings


app = QApplication(sys.argv)
app.setWindowIcon(QIcon(Settings.FAV_ICON_FILE_NAME))

Database.initialize(
    db_user=Settings.DB_USER,
    db_password=Settings.DB_PASSWORD,
    db_host=Settings.DB_HOST,
    db_port=Settings.DB_PORT,
    db_name=Settings.DB_NAME,
)

connection_success, _ = Database.check_connection()
if not connection_success:
    BaseWidget.show_error_pop_up(
        "Erro de Conexão",
        "Não foi possível conectar ao banco de dados.",
        "Por favor, entre em contato com o administrador do sistema.",
    )
    sys.exit(1)

menu_controller = MenuController()
login_controller = LoginController(menu_controller)

login_controller.show()

sys.exit(app.exec())
