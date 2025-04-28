from PySide6.QtWidgets import QFormLayout, QLabel, QLayout, QLineEdit

from common.gui.field.cpf_line_edit import CPFLineEdit
from common.gui.widget.base_add_widget import BaseAddWidget
from domain.driver.model import Driver


class DriverAddWidget(BaseAddWidget):
    def __init__(self, parent=None):
        super().__init__(
            model_class=Driver,
            width=300,
            height=150,
            parent=parent,
        )

    def _create_form_fields(self) -> QLayout:
        layout = QFormLayout()

        self.name_field = QLineEdit()
        layout.addRow(QLabel("Nome:"), self.name_field)

        self.cpf_field = CPFLineEdit()
        layout.addRow(QLabel("CPF:"), self.cpf_field)

        self.registration_number_field = QLineEdit()
        layout.addRow(QLabel("Registro:"), self.registration_number_field)

        return layout
