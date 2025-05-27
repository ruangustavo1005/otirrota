from PySide6.QtCore import QDate, QEvent, Qt
from PySide6.QtWidgets import (
    QApplication,
    QDateEdit,
    QFormLayout,
    QHBoxLayout,
    QLayout,
    QVBoxLayout,
    QWidget,
    QLabel,
)

from common.gui.widget.base_crud_widget import BaseCRUDWidget
from domain.roadmap.model import Roadmap
from domain.roadmap.suggest.drivers_vehicles_relation.drivers_group_widget import (
    DriversRelationGroupWidget,
)
from domain.roadmap.suggest.drivers_vehicles_relation.vehicles_group_widget import (
    VehiclesRelationGroupWidget,
)


class LoadingOverlay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("loadingOverlay")

        if parent:
            self.setGeometry(parent.rect())

        self.setStyleSheet(
            """
            #loadingOverlay {
                background-color: rgba(0, 0, 0, 180);
            }
            QLabel {
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 20px;
                background-color: rgba(50, 50, 50, 200);
                border-radius: 10px;
                border: 2px solid #ffffff;
            }
        """
        )

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.status_label = QLabel("Processando...")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setMinimumSize(600, 100)
        self.status_label.setWordWrap(True)

        layout.addWidget(self.status_label)
        self.setLayout(layout)

        self.hide()

    def show_with_message(self, message: str):
        self.status_label.setText(message)
        if self.parent():
            self.setGeometry(0, 0, self.parent().width(), self.parent().height())
        self.show()
        self.raise_()
        QApplication.processEvents()

    def update_message(self, message: str):
        self.status_label.setText(message)
        QApplication.processEvents()

    def hide_overlay(self):
        self.hide()

    def resizeEvent(self, event):
        if self.parent():
            self.setGeometry(0, 0, self.parent().width(), self.parent().height())
        super().resizeEvent(event)

    def showEvent(self, event):
        if self.parent():
            self.setGeometry(0, 0, self.parent().width(), self.parent().height())
        super().showEvent(event)


class SuggestRoadmapsWidget(BaseCRUDWidget[Roadmap]):
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

        self.loading_overlay = None

    def showEvent(self, event):
        super().showEvent(event)
        if self.loading_overlay is None:
            self.loading_overlay = LoadingOverlay(self)
            self.loading_overlay.resize(self.size())

    def show_loading(self, message: str = "Processando..."):
        if self.loading_overlay is None:
            self.loading_overlay = LoadingOverlay(self)

        self.setEnabled(False)
        self.loading_overlay.show_with_message(message)

    def update_loading_message(self, message: str):
        if self.loading_overlay:
            self.loading_overlay.update_message(message)

    def hide_loading(self):
        if self.loading_overlay:
            self.loading_overlay.hide_overlay()
        self.setEnabled(True)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, "loading_overlay") and self.loading_overlay:
            self.loading_overlay.setGeometry(0, 0, self.width(), self.height())

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
