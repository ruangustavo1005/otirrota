from PySide6.QtWidgets import (
    QAbstractItemView,
    QDateEdit,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLayout,
    QLineEdit,
    QTableWidget,
    QVBoxLayout,
)

from common.gui.field.custom_time_edit import TimeEdit
from common.gui.widget.base_view_widget import BaseViewWidget
from domain.roadmap.model import Roadmap


class RoadmapViewWidget(BaseViewWidget):
    def __init__(self, parent=None):
        super().__init__(
            model_class=Roadmap,
            width=650,
            height=500,
            parent=parent,
        )

    def _create_form_fields(self) -> QLayout:
        layout = QVBoxLayout()

        layout.addLayout(self._create_first_form_part_layout())
        layout.addWidget(self._create_scheduling_table_group_box())
        layout.addLayout(self._create_second_form_part_layout())

        return layout

    def _create_first_form_part_layout(self) -> QLayout:
        layout = QFormLayout()

        self.date_field = QDateEdit()
        self.date_field.setDisplayFormat("dd/MM/yyyy")
        self.date_field.setFixedWidth(100)
        self.date_field.setDisabled(True)
        layout.addRow(QLabel("Data:"), self.date_field)

        self.driver_field = QLineEdit()
        self.driver_field.setDisabled(True)
        layout.addRow(QLabel("Motorista:"), self.driver_field)

        self.vehicle_field = QLineEdit()
        self.vehicle_field.setDisabled(True)
        layout.addRow(QLabel("Veículo:"), self.vehicle_field)

        return layout

    def _create_scheduling_table_group_box(self) -> QGroupBox:
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
        self.schedulings_table.setDisabled(True)

        scheduling_table_layout = QVBoxLayout()
        scheduling_table_layout.addWidget(self.schedulings_table)

        group_box = QGroupBox("Agendamentos")
        group_box.setLayout(scheduling_table_layout)

        return group_box

    def _create_second_form_part_layout(self) -> QLayout:
        layout = QFormLayout()
        times_layout = QHBoxLayout()

        self.departure_time_field = TimeEdit(step_minutes=15)
        self.departure_time_field.setDisplayFormat("HH:mm")
        self.departure_time_field.setFixedWidth(50)
        self.departure_time_field.setDisabled(True)
        times_layout.addWidget(self.departure_time_field)

        times_layout.addWidget(QLabel("Chegada:"))
        self.arrival_time_field = TimeEdit(step_minutes=15)
        self.arrival_time_field.setDisplayFormat("HH:mm")
        self.arrival_time_field.setFixedWidth(50)
        self.arrival_time_field.setDisabled(True)
        times_layout.addWidget(self.arrival_time_field)

        layout.addRow(QLabel("Saída:"), times_layout)

        self.creation_user_field = QLineEdit()
        self.creation_user_field.setReadOnly(True)
        layout.addRow(QLabel("Usuário que criou:"), self.creation_user_field)

        return layout
