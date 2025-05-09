from typing import Optional

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QHBoxLayout, QLineEdit, QPushButton, QWidget

from common.gui.field.cpf_line_edit import CPFLineEdit
from common.gui.field.phone_line_edit import PhoneLineEdit
from domain.companion.model import Companion


class CompanionRowWidget(QWidget):
    remove_requested = Signal(object)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self) -> None:
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        self.id_field = QLineEdit()
        self.id_field.hide()
        layout.addWidget(self.id_field, 0)

        self.name_field = QLineEdit()
        layout.addWidget(self.name_field, 5)

        self.cpf_field = CPFLineEdit()
        layout.addWidget(self.cpf_field, 3)

        self.phone_field = PhoneLineEdit()
        layout.addWidget(self.phone_field, 3)

        self.remove_button = QPushButton("Remover Linha")
        self.remove_button.clicked.connect(lambda: self.remove_requested.emit(self))
        layout.addWidget(self.remove_button, 2)

        self.setLayout(layout)

    def get_data(self, index: int) -> Optional[Companion]:
        cpf = self.cpf_field.get_cpf_numbers()
        if cpf and not self.cpf_field.is_valid_cpf():
            raise ValueError(f"O CPF {cpf} de acompanhante {index + 1} é inválido")

        phone = self.phone_field.get_phone_number()
        if phone and not self.phone_field.is_valid_phone():
            raise ValueError(
                f"O telefone {phone} de acompanhante {index + 1} é inválido"
            )

        name = self.name_field.text().strip()
        if not name:
            if cpf or phone:
                raise ValueError(f"O nome do acompanhante {index + 1} é obrigatório")
            return None

        companion = Companion(name=name, cpf=cpf, phone=phone)
        if self.id_field.text():
            companion.id = int(self.id_field.text())
        return companion

    def set_data(self, companion: Companion) -> None:
        self.id_field.setText(str(companion.id))
        self.name_field.setText(companion.name)
        self.cpf_field.setText(companion.format_cpf())
        self.phone_field.setText(companion.format_phone())
