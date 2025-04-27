from PySide6.QtWidgets import QFormLayout, QLabel, QLayout, QLineEdit

from common.gui.widget.base_add_widget import BaseAddWidget
from routines.user.model import User


class UserAddWidget(BaseAddWidget):
    def __init__(self, parent=None):
        super().__init__(
            model_class=User,
            width=300,
            height=150,
            parent=parent,
        )

    def _create_form_fields(self) -> QLayout:
        layout = QFormLayout()

        self.name_field = QLineEdit()
        layout.addRow(QLabel("Nome:"), self.name_field)

        self.user_name_field = QLineEdit()
        layout.addRow(QLabel("Login:"), self.user_name_field)

        self.password_field = QLineEdit()
        self.password_field.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addRow(QLabel("Senha:"), self.password_field)

        self.confirm_password_field = QLineEdit()
        self.confirm_password_field.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addRow(QLabel("Confirmação:"), self.confirm_password_field)

        return layout
