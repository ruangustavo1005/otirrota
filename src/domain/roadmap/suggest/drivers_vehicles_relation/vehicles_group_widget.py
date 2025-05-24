from typing import List

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from domain.roadmap.suggest.drivers_vehicles_relation.vehicles_row_widget import (
    VehiclesRelationRowWidget,
)
from domain.vehicle.model import Vehicle


class VehiclesRelationGroupWidget(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.relation_rows: List[VehiclesRelationRowWidget] = []
        self.setup_ui()

    def setup_ui(self) -> None:
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.group_box = QGroupBox("Relação de Veículos")
        self.group_box.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)

        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(5, 5, 5, 5)
        content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        content_layout.setSpacing(5)

        header_layout = QHBoxLayout()
        use_label = QLabel("Usar?")
        use_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(use_label, 1)
        vehicle_label = QLabel("Veículo")
        vehicle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(vehicle_label, 9)
        content_layout.addLayout(header_layout)

        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.setSpacing(5)
        scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.relations_layout = QVBoxLayout()
        self.relations_layout.setSpacing(5)
        self.relations_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        scroll_layout.addLayout(self.relations_layout)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setMaximumHeight(500)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        content_layout.addWidget(scroll_area)

        group_layout = QVBoxLayout()
        group_layout.addWidget(content_widget)
        self.group_box.setLayout(group_layout)

        main_layout.addWidget(self.group_box)
        self.setLayout(main_layout)

    def add_relation_row(self, vehicle: Vehicle) -> None:
        new_row = VehiclesRelationRowWidget()
        self.relations_layout.addWidget(new_row)
        self.relation_rows.append(new_row)
        new_row.set_data(vehicle)

    def get_relations(self) -> List[Vehicle]:
        relations = []
        for row in self.relation_rows:
            relation = row.get_data()
            if relation:
                relations.append(relation)
        return relations

    def set_relations(self, relations: List[Vehicle]) -> None:
        for row in self.relation_rows[:]:
            self.relations_layout.removeWidget(row)
            self.relation_rows.remove(row)
            row.deleteLater()

        for relation in relations:
            self.add_relation_row(relation)
