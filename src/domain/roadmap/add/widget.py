from typing import List

from PySide6.QtCore import QDate, QEvent, Qt, QTime
from PySide6.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QDateEdit,
    QFormLayout,
    QFrame,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLayout,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
)

from common.gui.field.combo_box import ComboBox
from common.gui.field.custom_time_edit import TimeEdit
from common.gui.widget.base_add_widget import BaseAddWidget
from domain.driver.field.active_drivers_combo_box import ActiveDriversComboBox
from domain.roadmap.model import Roadmap
from domain.scheduling.model import Scheduling
from domain.vehicle.model import Vehicle


class RoadmapAddWidget(BaseAddWidget):
    def __init__(self, parent=None):
        super().__init__(
            model_class=Roadmap,
            width=650,
            height=750,
            parent=parent,
        )
        qApp = QApplication.instance()
        qApp.installEventFilter(self)

    def eventFilter(self, watched, event):
        if event.type() == QEvent.MouseButtonRelease:
            if (
                hasattr(self, "departure_time_field")
                and self.departure_time_field.underMouse()
            ):
                self.departure_time_field.setSelectedSection(
                    self.departure_time_field.currentSection()
                )
                return False
            if (
                hasattr(self, "arrival_time_field")
                and self.arrival_time_field.underMouse()
            ):
                self.arrival_time_field.setSelectedSection(
                    self.arrival_time_field.currentSection()
                )

        return super().eventFilter(watched, event)

    def _create_form_fields(self) -> QLayout:
        layout = QVBoxLayout()

        layout.addLayout(self._create_first_form_part_layout())
        layout.addWidget(self._create_scheduling_table_group_box())
        layout.addLayout(self._create_second_form_part_layout())

        return layout

    def _create_first_form_part_layout(self) -> QLayout:
        layout = QFormLayout()

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
        self.date_field.dateChanged.connect(self._fill_schedulings_combo_box)
        layout.addRow(QLabel("Data:"), self.date_field)

        self.driver_combo_box = ActiveDriversComboBox()
        self.driver_combo_box.currentIndexChanged.connect(self._on_driver_changed)
        layout.addRow(QLabel("Motorista:"), self.driver_combo_box)

        self.vehicle_combo_box = ComboBox(model_class=Vehicle)
        layout.addRow(QLabel("Veículo:"), self.vehicle_combo_box)

        return layout

    def _on_driver_changed(self, index: int) -> None:
        driver = self.driver_combo_box.get_data()[index - 1]
        if driver is not None:
            vehicle = next(
                (
                    v
                    for v in self.vehicle_combo_box.get_data()
                    if v.default_driver_id == driver.id
                ),
                None,
            )
            if vehicle is not None:
                self.vehicle_combo_box.setCurrentIndexByData(vehicle)

    def _add_scheduling_to_table(self) -> None:
        scheduling = self.scheduling_combo_box.get_current_data()
        if scheduling is not None:
            row_count = self.schedulings_table.rowCount()
            self.schedulings_table.insertRow(row_count)
            self.schedulings_table.setItem(
                row_count, 0, QTableWidgetItem(str(scheduling.id))
            )
            self.schedulings_table.setItem(
                row_count, 1, QTableWidgetItem(scheduling.get_description())
            )
            self._fill_schedulings_combo_box()

    def _fill_schedulings_combo_box(self) -> None:
        self.scheduling_combo_box.fill(
            date=self.date_field.date().toPython(),
            ids_ignore=self._get_scheduling_ids_from_table(),
        )

    def _get_scheduling_ids_from_table(self) -> List[int]:
        scheduling_ids = []
        for row in range(self.schedulings_table.rowCount()):
            scheduling_id = self.schedulings_table.item(row, 0).data(Qt.DisplayRole)
            if scheduling_id:
                scheduling_ids.append(int(scheduling_id))
        return scheduling_ids

    def _create_scheduling_table_group_box(self) -> QGroupBox:
        scheduling_table_layout = QVBoxLayout()

        scheduling_combo_box_layout = QHBoxLayout()
        self.scheduling_combo_box = ComboBox(model_class=Scheduling, load=False)
        self.scheduling_combo_box.currentIndexChanged.connect(
            self._on_scheduling_combo_box_changed
        )
        scheduling_combo_box_label = QLabel("Selecione um agendamento:")
        scheduling_combo_box_label.setFixedWidth(160)
        scheduling_combo_box_layout.addWidget(scheduling_combo_box_label)
        scheduling_combo_box_layout.addWidget(self.scheduling_combo_box)
        scheduling_table_layout.addLayout(scheduling_combo_box_layout)

        scheduling_buttons_layout = QHBoxLayout()
        self._view_scheduling_button = QPushButton("Visualizar Agendamento")
        self.add_scheduling_button = QPushButton("Adicionar Agendamento ao Roteiro")
        self.add_scheduling_button.clicked.connect(self._add_scheduling_to_table)
        scheduling_buttons_layout.addWidget(self._view_scheduling_button)
        scheduling_buttons_layout.addWidget(self.add_scheduling_button)
        scheduling_table_layout.addLayout(scheduling_buttons_layout)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        scheduling_table_layout.addWidget(line)

        self.schedulings_table = QTableWidget()
        self.schedulings_table.setColumnCount(2)
        self.schedulings_table.setHorizontalHeaderLabels(["ID", "Agendamento"])
        self.schedulings_table.setColumnWidth(0, 1)
        self.schedulings_table.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeMode.Fixed
        )
        self.schedulings_table.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.ResizeMode.Stretch
        )
        self.schedulings_table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.schedulings_table.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )
        self.schedulings_table.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )
        self.schedulings_table.itemSelectionChanged.connect(
            self._on_scheduling_selection_changed
        )
        scheduling_table_layout.addWidget(self.schedulings_table)

        self.remove_scheduling_button = QPushButton("Remover Agendamento Selecionado")
        self.remove_scheduling_button.setFixedWidth(230)
        self.remove_scheduling_button.setEnabled(False)
        self.remove_scheduling_button.clicked.connect(self._remove_selected_scheduling)
        remove_scheduling_layout = QHBoxLayout()
        remove_scheduling_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        remove_scheduling_layout.addWidget(self.remove_scheduling_button)
        scheduling_table_layout.addLayout(remove_scheduling_layout)

        group_box = QGroupBox("Agendamentos")
        group_box.setLayout(scheduling_table_layout)

        return group_box

    def _on_scheduling_combo_box_changed(self) -> None:
        if self.scheduling_combo_box.get_current_data() is not None:
            self._view_scheduling_button.setEnabled(True)
            self.add_scheduling_button.setEnabled(True)
        else:
            self._view_scheduling_button.setEnabled(False)
            self.add_scheduling_button.setEnabled(False)

    def _on_scheduling_selection_changed(self) -> None:
        selected_rows = self.schedulings_table.selectedIndexes()
        self.remove_scheduling_button.setEnabled(len(selected_rows) > 0)

    def _remove_selected_scheduling(self) -> None:
        selected_rows = self.schedulings_table.selectedIndexes()
        if selected_rows:
            self.schedulings_table.removeRow(selected_rows[0].row())
            self._fill_schedulings_combo_box()

    def _create_second_form_part_layout(self) -> QLayout:
        layout = QFormLayout()
        times_layout = QHBoxLayout()

        self.departure_time_field = TimeEdit(step_minutes=15)
        self.departure_time_field.setTimeRange(QTime(0, 0, 0), QTime(23, 59, 0))
        self.departure_time_field.setDisplayFormat("HH:mm")
        self.departure_time_field.setCurrentSection(TimeEdit.MinuteSection)
        self.departure_time_field.setTime(QTime(1, 0))
        self.departure_time_field.setFixedWidth(50)
        times_layout.addWidget(self.departure_time_field)

        times_layout.addWidget(QLabel("Chegada:"))
        self.arrival_time_field = TimeEdit(step_minutes=15)
        self.arrival_time_field.setTimeRange(QTime(0, 0, 0), QTime(23, 59, 0))
        self.arrival_time_field.setDisplayFormat("HH:mm")
        self.arrival_time_field.setCurrentSection(TimeEdit.MinuteSection)
        self.arrival_time_field.setTime(QTime(1, 0))
        self.arrival_time_field.setFixedWidth(50)
        times_layout.addWidget(self.arrival_time_field)

        self.calculate_departure_arrival_button = QPushButton("Sugerir Horários")
        times_layout.addWidget(self.calculate_departure_arrival_button)

        layout.addRow(QLabel("Saída:"), times_layout)

        return layout
