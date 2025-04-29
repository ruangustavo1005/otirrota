from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QLabel, QLineEdit

from common.gui.field.cpf_line_edit import CPFLineEdit
from common.gui.widget.base_list_widget import BaseListWidget
from domain.patient.model import Patient


class PatientListWidget(BaseListWidget[Patient]):
    def __init__(
        self,
        parent=None,
    ):
        super().__init__(
            model_class=Patient,
            width=1000,
            height=738,
            parent=parent,
        )

    def _create_filter_fields(self, filter_area_layout: QHBoxLayout) -> None:
        nome_label = QLabel("Nome:")
        nome_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        nome_label.setFixedWidth(40)
        filter_area_layout.addWidget(nome_label)

        self.nome_filter = QLineEdit()
        self.nome_filter.setFixedWidth(100)
        self.nome_filter.returnPressed.connect(self.update_button.click)
        filter_area_layout.addWidget(self.nome_filter)

        cpf_label = QLabel("CPF:")
        cpf_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        cpf_label.setFixedWidth(30)
        filter_area_layout.addWidget(cpf_label)

        self.cpf_filter = CPFLineEdit()
        self.cpf_filter.setFixedWidth(100)
        self.cpf_filter.returnPressed.connect(self.update_button.click)
        filter_area_layout.addWidget(self.cpf_filter)

    def _create_actions_area(self) -> QHBoxLayout:
        layout = super()._create_actions_area()
        self.view_button.setVisible(False)
        return layout
