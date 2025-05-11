from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QDateTimeEdit,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLayout,
    QLineEdit,
    QTextEdit,
    QVBoxLayout,
)

from common.gui.field.combo_box import ComboBox
from common.gui.field.custom_time_edit import TimeEdit
from common.gui.widget.base_view_widget import BaseViewWidget
from domain.companion.widget.group_widget import CompanionsGroupWidget
from domain.purpose.model import Purpose
from domain.scheduling.model import Scheduling


class SchedulingViewWidget(BaseViewWidget):
    def __init__(self, parent=None):
        super().__init__(
            model_class=Scheduling,
            width=650,
            height=650,
            parent=parent,
        )

    def _create_form_fields(self) -> QLayout:
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)

        form_layout = QFormLayout()

        self.datetime_field = QDateTimeEdit()
        self.datetime_field.setDisplayFormat("dd/MM/yyyy HH:mm")
        self.datetime_field.setFixedWidth(120)
        self.datetime_field.setDisabled(True)

        self.average_duration_field = TimeEdit(step_minutes=30)
        self.average_duration_field.setDisplayFormat("HH:mm")
        self.average_duration_field.setFixedWidth(50)
        self.average_duration_field.setDisabled(True)

        time_layout = QHBoxLayout()
        time_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        time_layout.addWidget(self.datetime_field)
        average_duration_label = QLabel("Duração Estimada:")
        average_duration_label.setFixedWidth(100)
        time_layout.addWidget(average_duration_label)
        time_layout.addWidget(self.average_duration_field)
        form_layout.addRow(QLabel("Data e Hora:"), time_layout)

        self.patient_field = QLineEdit()
        self.patient_field.setDisabled(True)
        form_layout.addRow(QLabel("Paciente:"), self.patient_field)

        self.location_field = QLineEdit()
        self.location_field.setDisabled(True)
        form_layout.addRow(QLabel("Localização:"), self.location_field)

        self.purpose_field = QLineEdit()
        self.purpose_field.setDisabled(True)
        form_layout.addRow(QLabel("Finalidade:"), self.purpose_field)

        self.sensitive_patient_checkbox = QCheckBox("")
        self.sensitive_patient_checkbox.setDisabled(True)
        form_layout.addRow(
            QLabel("Paciente Sensível?"), self.sensitive_patient_checkbox
        )

        self.description_field = QTextEdit()
        self.description_field.setFixedHeight(100)
        self.description_field.setDisabled(True)
        form_layout.addRow(QLabel("Descrição:"), self.description_field)

        main_layout.addLayout(form_layout)

        self.companions_widget = CompanionsGroupWidget()
        self.companions_widget.set_disabled(True)
        main_layout.addWidget(self.companions_widget)

        main_layout.addStretch(1)

        return main_layout
