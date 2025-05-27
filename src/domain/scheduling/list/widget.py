from enum import Enum

from PySide6.QtCore import QDate, Qt
from PySide6.QtWidgets import QComboBox, QDateEdit, QHBoxLayout, QHeaderView, QLabel

from common.gui.field.boolean_combo_box import BooleanComboBox
from common.gui.widget.base_list_widget import BaseListWidget
from domain.scheduling.model import Scheduling


class SchedulingListWidget(BaseListWidget[Scheduling]):
    def __init__(
        self,
        parent=None,
    ):
        super().__init__(
            model_class=Scheduling,
            width=1500,
            height=900,
            parent=parent,
        )

    def _create_filter_fields(self, filter_area_layout: QHBoxLayout) -> None:
        type_label = QLabel("Tipo:")
        type_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        type_label.setFixedWidth(40)
        filter_area_layout.addWidget(type_label)

        self.type_filter = QComboBox()
        for filter_type in SchedulingDateTypeFilterEnum:
            self.type_filter.addItem(filter_type.value, filter_type.name)
        self.type_filter.currentIndexChanged.connect(self.update_button.click)
        filter_area_layout.addWidget(self.type_filter)

        date_label = QLabel("Data:")
        date_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        date_label.setFixedWidth(40)
        filter_area_layout.addWidget(date_label)

        self.date_filter = QDateEdit()
        self.date_filter.setFixedWidth(100)
        self.date_filter.setCalendarPopup(True)
        self.date_filter.setDisplayFormat("dd/MM/yyyy")
        self.date_filter.setDate(QDate.currentDate())
        self.date_filter.dateChanged.connect(self.update_button.click)
        filter_area_layout.addWidget(self.date_filter)

        roadmap_exists_label = QLabel("Possui Roteiro?")
        roadmap_exists_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        roadmap_exists_label.setFixedWidth(100)
        filter_area_layout.addWidget(roadmap_exists_label)

        self.roadmap_exists_filter = BooleanComboBox()
        self.roadmap_exists_filter.currentIndexChanged.connect(self.update_button.click)
        self.roadmap_exists_filter.setFixedWidth(100)
        filter_area_layout.addWidget(self.roadmap_exists_filter)

    def _configure_table_columns(self, header: QHeaderView) -> None:
        super()._configure_table_columns(header)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        header.resizeSection(0, 110)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        header.resizeSection(2, 150)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        header.resizeSection(3, 110)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)
        header.resizeSection(5, 110)
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed)
        header.resizeSection(6, 100)


class SchedulingDateTypeFilterEnum(str, Enum):
    DAY = "Dia"
    WEEK = "Semana"
    MONTH = "Mês"
    YEAR = "Ano"
