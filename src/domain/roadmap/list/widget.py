from enum import Enum

from PySide6.QtCore import QDate, Qt
from PySide6.QtWidgets import (
    QComboBox,
    QDateEdit,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QPushButton,
)

from common.gui.widget.base_list_widget import BaseListWidget
from domain.roadmap.model import Roadmap


class RoadmapListWidget(BaseListWidget[Roadmap]):
    def __init__(
        self,
        parent=None,
    ):
        super().__init__(
            model_class=Roadmap,
            width=1200,
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
        for filter_type in RoadmapDateTypeFilterEnum:
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

    def _create_actions_area(self) -> QHBoxLayout:
        layout = super()._create_actions_area()

        self.suggest_roadmaps_button = QPushButton("Sugerir Roteiros")
        self.suggest_roadmaps_button.setFixedWidth(130)
        layout.addWidget(self.suggest_roadmaps_button)

        return layout

    def _configure_table_columns(self, header: QHeaderView) -> None:
        super()._configure_table_columns(header)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        header.resizeSection(2, 90)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        header.resizeSection(3, 60)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        header.resizeSection(4, 60)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)
        header.resizeSection(5, 120)


class RoadmapDateTypeFilterEnum(str, Enum):
    DAY = "Dia"
    WEEK = "Semana"
    MONTH = "Mês"
    YEAR = "Ano"
