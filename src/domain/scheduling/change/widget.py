from PySide6.QtCore import QDateTime, QEvent, Qt, QTime
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QDateTimeEdit,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLayout,
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

        form_layout = QFormLayout()

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
        form_layout.addRow(QLabel("Data e Hora:"), time_layout)

        self.patient_field = SearchLineEdit(model_class=Patient)
        form_layout.addRow(QLabel("Paciente:"), self.patient_field)

        self.location_field = SearchLineEdit(model_class=Location)
        form_layout.addRow(QLabel("Localização:"), self.location_field)

        self.purpose_field = ComboBox(model_class=Purpose, default_none=False)
        form_layout.addRow(QLabel("Finalidade:"), self.purpose_field)

        self.sensitive_patient_checkbox = QCheckBox("")
        form_layout.addRow(
            QLabel("Paciente Sensível?"), self.sensitive_patient_checkbox
        )

        self.description_field = QTextEdit()
        self.description_field.setFixedHeight(100)
        form_layout.addRow(QLabel("Descrição:"), self.description_field)

        main_layout.addLayout(form_layout)

        self.companions_widget = CompanionsGroupWidget()
        main_layout.addWidget(self.companions_widget)

        main_layout.addStretch(1)

        return main_layout

    def _focus_time_section(self, date):
        self.datetime_field.setCurrentSection(QDateTimeEdit.HourSection)
        self.datetime_field.setSelectedSection(QDateTimeEdit.HourSection)
