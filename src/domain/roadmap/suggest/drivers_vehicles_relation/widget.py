from PySide6.QtCore import QDate, QEvent, Qt
from PySide6.QtWidgets import (
    QApplication,
    QDateEdit,
    QFormLayout,
    QHBoxLayout,
    QLayout,
    QVBoxLayout,
)

from common.gui.widget.base_crud_widget import BaseCRUDWidget
from domain.roadmap.model import Roadmap
from domain.roadmap.suggest.drivers_vehicles_relation.drivers_group_widget import (
    DriversRelationGroupWidget,
)
from domain.roadmap.suggest.drivers_vehicles_relation.vehicles_group_widget import (
    VehiclesRelationGroupWidget,
)


class DriversVehiclesRelationWidget(BaseCRUDWidget[Roadmap]):
    def __init__(self, parent=None):
        super().__init__(
            model_class=Roadmap,
            title="Informe os Dados para Geração dos Roteiros",
            width=800,
            height=600,
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
        layout.addLayout(self.__create_date_layout())
        layout.addLayout(self.__create_drivers_vehicles_relation_layout())
        return layout

    def __create_date_layout(self) -> QFormLayout:
        date_layout = QFormLayout()
        self.date_field = QDateEdit()
        self.date_field.setCalendarPopup(True)
        self.date_field.setDisplayFormat("dd/MM/yyyy")
        current_date = QDate.currentDate()
        self.date_field.setDate(
            current_date.addDays(
                3 if current_date.dayOfWeek() == Qt.DayOfWeek.Friday.value else 1
            )
        )
        self.date_field.setFixedWidth(100)
        date_layout.addRow("Sugerir roteiros para o dia:", self.date_field)
        return date_layout

    def __create_drivers_vehicles_relation_layout(self) -> QHBoxLayout:
        layout = QHBoxLayout()
        self.drivers_relation_group_widget = DriversRelationGroupWidget()
        layout.addWidget(self.drivers_relation_group_widget)
        self.vehicles_relation_group_widget = VehiclesRelationGroupWidget()
        layout.addWidget(self.vehicles_relation_group_widget)
        return layout

    def _get_submit_button_text(self):
        return "Gerar Sugestões"
