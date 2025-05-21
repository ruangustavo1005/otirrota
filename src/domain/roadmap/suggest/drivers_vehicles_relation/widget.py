from PySide6.QtWidgets import QApplication, QLayout, QVBoxLayout, QDateEdit, QFormLayout
from PySide6.QtCore import QEvent, QDate, Qt
from common.gui.widget.base_crud_widget import BaseCRUDWidget
from domain.roadmap.model import Roadmap
from domain.roadmap.suggest.drivers_vehicles_relation.group_widget import (
    DriversVehiclesRelationGroupWidget,
)


class DriversVehiclesRelationWidget(BaseCRUDWidget[Roadmap]):
    def __init__(self, parent=None):
        super().__init__(
            model_class=Roadmap,
            title="Informe os Veículos e Motoristas para Geração dos Roteiros",
            width=700,
            height=500,
            parent=parent,
        )
        self.submit_button.setFixedWidth(130)
        qApp = QApplication.instance()
        qApp.installEventFilter(self)

    def eventFilter(self, watched, event):
        if event.type() == QEvent.MouseButtonRelease:
            if hasattr(self, "datetime_field") and self.datetime_field.underMouse():
                self.datetime_field.setSelectedSection(
                    self.datetime_field.currentSection()
                )
                return False

        return super().eventFilter(watched, event)

    def _create_form_fields(self) -> QLayout:
        layout = QVBoxLayout()

        date_layout = QFormLayout()
        self.date_field = QDateEdit()
        self.date_field.setCalendarPopup(True)
        self.date_field.setDisplayFormat("dd/MM/yyyy")
        current_date = QDate.currentDate()
        self.date_field.setDate(
            current_date.addDays(
                3 if current_date.dayOfWeek() == Qt.DayOfWeek.Friday else 1
            )
        )
        self.date_field.setFixedWidth(100)
        date_layout.addRow("Sugerir roteiros para o dia:", self.date_field)
        layout.addLayout(date_layout)

        self.relations_area = DriversVehiclesRelationGroupWidget()
        layout.addWidget(self.relations_area)

        return layout

    def _get_submit_button_text(self):
        return "Gerar Sugestões"
