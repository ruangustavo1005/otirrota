from enum import Enum

from PySide6.QtCore import QDate, Qt
from PySide6.QtWidgets import QComboBox, QDateEdit, QHBoxLayout, QLabel

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


class SchedulingDateTypeFilterEnum(str, Enum):
    DAY = "Dia"
    WEEK = "Semana"
    MONTH = "Mês"
    YEAR = "Ano"
