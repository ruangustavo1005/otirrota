from PySide6.QtWidgets import QFormLayout, QLabel, QLayout, QLineEdit

from common.gui.field.cpf_line_edit import CPFLineEdit
from common.gui.field.phone_line_edit import PhoneLineEdit
from common.gui.widget.base_change_widget import BaseChangeWidget
from domain.patient.model import Patient


class PatientChangeWidget(BaseChangeWidget):
    def __init__(self, parent=None):
        super().__init__(
            model_class=Patient,
            width=300,
            height=80,
            parent=parent,
        )

    def _create_form_fields(self) -> QLayout:
        layout = QFormLayout()

        self.name_field = QLineEdit()
        layout.addRow(QLabel("Nome:"), self.name_field)

        self.cpf_field = CPFLineEdit()
        layout.addRow(QLabel("CPF:"), self.cpf_field)

        self.phone_field = PhoneLineEdit()
        layout.addRow(QLabel("Telefone:"), self.phone_field)

        return layout
