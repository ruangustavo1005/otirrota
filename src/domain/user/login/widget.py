from PySide6.QtWidgets import QFormLayout, QHBoxLayout, QLabel, QLayout, QLineEdit

from common.gui.widget.base_crud_widget import BaseCRUDWidget
from domain.user.model import User


class LoginWidget(BaseCRUDWidget[User]):
    def __init__(self):
        super().__init__(
            model_class=User,
            title="Login",
            width=250,
            height=100,
        )

    def _create_form_fields(self) -> QLayout:
        layout = QFormLayout()

        self.user_name_field = QLineEdit()
        layout.addRow(QLabel("Login"), self.user_name_field)

        self.password_field = QLineEdit()
        self.password_field.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addRow(QLabel("Senha"), self.password_field)

        return layout

    def _create_actions_area(self) -> QHBoxLayout:
        layout = super()._create_actions_area()

        self.user_name_field.returnPressed.connect(self.submit_button.click)
        self.password_field.returnPressed.connect(self.submit_button.click)

        return layout

    def _get_submit_button_text(self):
        return "Entrar"
