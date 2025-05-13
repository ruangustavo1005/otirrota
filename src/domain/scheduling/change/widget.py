from typing import Optional

from PySide6.QtCore import QEvent, Qt, QTime
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QDateTimeEdit,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLayout,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
)

from common.gui.field.combo_box import ComboBox
from common.gui.field.custom_time_edit import TimeEdit
from common.gui.field.search_line_edit import SearchLineEdit
from common.gui.widget.base_change_widget import BaseChangeWidget
from domain.companion.widget.group_widget import CompanionsGroupWidget
from domain.location.model import Location
from domain.patient.model import Patient
from domain.purpose.model import Purpose
from domain.scheduling.model import Scheduling


class SchedulingChangeWidget(BaseChangeWidget):
    def __init__(self, parent=None):
        super().__init__(
            model_class=Scheduling,
            width=650,
            height=650,
            parent=parent,
        )
        qApp = QApplication.instance()
        qApp.installEventFilter(self)

    def eventFilter(self, watched, event):
        if event.type() == QEvent.MouseButtonRelease:
            if hasattr(self, "datetime_field") and self.datetime_field.underMouse():
                self.datetime_field.setSelectedSection(
                    self.datetime_field.currentSection()
                )
                return False

            if (
                hasattr(self, "average_duration_field")
                and self.average_duration_field.underMouse()
            ):
                self.average_duration_field.setSelectedSection(
                    self.average_duration_field.currentSection()
                )
                return False

        return super().eventFilter(watched, event)

    def _create_form_fields(self) -> QLayout:
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)

        self.form_layout = QFormLayout()

        self.datetime_field = QDateTimeEdit()
        self.datetime_field.setCalendarPopup(True)
        self.datetime_field.setDisplayFormat("dd/MM/yyyy HH:mm")
        self.datetime_field.setFixedWidth(120)
        self.datetime_field.dateChanged.connect(self._focus_time_section)

        self.average_duration_field = TimeEdit(step_minutes=30)
        self.average_duration_field.setTimeRange(QTime(0, 0, 0), QTime(12, 0, 0))
        self.average_duration_field.setDisplayFormat("HH:mm")
        self.average_duration_field.setCurrentSection(TimeEdit.MinuteSection)
        self.average_duration_field.setFixedWidth(50)

        time_layout = QHBoxLayout()
        time_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        time_layout.addWidget(self.datetime_field)
        average_duration_label = QLabel("Duração Estimada:")
        average_duration_label.setFixedWidth(100)
        time_layout.addWidget(average_duration_label)
        time_layout.addWidget(self.average_duration_field)
        self.form_layout.addRow(QLabel("Data e Hora:"), time_layout)

        self.location_field = SearchLineEdit(model_class=Location)
        self.add_location_button = QPushButton("Adicionar Localização")
        self.add_location_button.setFixedWidth(150)
        location_layout = QHBoxLayout()
        location_layout.addWidget(self.location_field)
        location_layout.addWidget(self.add_location_button)
        self.form_layout.addRow(QLabel("Localização:"), location_layout)

        self.purpose_field = ComboBox(model_class=Purpose, default_none=False)
        self.form_layout.addRow(QLabel("Finalidade:"), self.purpose_field)

        self.patient_field = SearchLineEdit(model_class=Patient)
        self.patient_field.model_changed.connect(self._on_patient_changed)
        self.add_patient_button = QPushButton("Adicionar Paciente")
        self.add_patient_button.setFixedWidth(150)
        patient_layout = QHBoxLayout()
        patient_layout.addWidget(self.patient_field)
        patient_layout.addWidget(self.add_patient_button)
        self.form_layout.addRow(QLabel("Paciente:"), patient_layout)

        self.sensitive_patient_checkbox = QCheckBox("Paciente Sensível")
        self.form_layout.addRow(QLabel(""), self.sensitive_patient_checkbox)

        self.companions_widget = CompanionsGroupWidget()
        self.form_layout.addWidget(self.companions_widget)

        self.description_field = QTextEdit()
        self.description_field.setFixedHeight(100)
        self.form_layout.addRow(QLabel("Descrição:"), self.description_field)

        main_layout.addLayout(self.form_layout)
        main_layout.addStretch(1)

        return main_layout

    def _focus_time_section(self, date):
        self.datetime_field.setCurrentSection(QDateTimeEdit.HourSection)
        self.datetime_field.setSelectedSection(QDateTimeEdit.HourSection)

    def _on_patient_changed(self, patient: Optional[Patient]):
        if patient is None:
            self.form_layout.setRowVisible(self.sensitive_patient_checkbox, False)
            self.sensitive_patient_checkbox.setChecked(False)
            self.companions_widget.hide()
            self.companions_widget.set_companions([])
        else:
            self.form_layout.setRowVisible(self.sensitive_patient_checkbox, True)
            self.companions_widget.show()
