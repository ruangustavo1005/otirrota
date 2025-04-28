from PySide6.QtWidgets import QCheckBox, QFormLayout, QLabel, QLayout, QLineEdit

from common.gui.widget.base_change_widget import BaseChangeWidget
from domain.user.model import User


class UserChangeWidget(BaseChangeWidget):
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

        layout.addRow(
            QLabel("Atenção: Deixe a senha em branco para manter a senha atual.")
        )

        self.password_field = QLineEdit()
        self.password_field.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addRow(QLabel("Senha:"), self.password_field)

        self.confirm_password_field = QLineEdit()
        self.confirm_password_field.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addRow(QLabel("Confirmação:"), self.confirm_password_field)

        self.active_field = QCheckBox()
        layout.addRow(QLabel("Ativo:"), self.active_field)

        return layout
