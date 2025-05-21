from typing import List, Optional

from PySide6.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QSizePolicy,
    QScrollArea,
    QFrame,
)
from PySide6.QtCore import Qt

from domain.roadmap.suggest.drivers_vehicles_relation.model import (
    DriversVehiclesRelation,
)
from domain.roadmap.suggest.drivers_vehicles_relation.row_widget import (
    DriversVehiclesRelationRowWidget,
)


class DriversVehiclesRelationGroupWidget(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.relation_rows: List[DriversVehiclesRelationRowWidget] = []
        self.relations: List[DriversVehiclesRelation] = []
        self.setup_ui()

    def setup_ui(self) -> None:
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.group_box = QGroupBox("Veículos e Motoristas")
        self.group_box.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)

        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(5, 5, 5, 5)
        content_layout.setAlignment(Qt.AlignTop)
        content_layout.setSpacing(5)

        header_layout = QHBoxLayout()
        header_layout.addWidget(QLabel("Motorista"), 5)
        header_layout.addWidget(QLabel("Veículo"), 5)
        header_layout.addWidget(QLabel("Plantão?"), 2)
        header_layout.addWidget(QLabel(""), 2)
        content_layout.addLayout(header_layout)

        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.setSpacing(5)
        scroll_layout.setAlignment(Qt.AlignTop)

        self.relations_layout = QVBoxLayout()
        self.relations_layout.setSpacing(5)
        self.relations_layout.setAlignment(Qt.AlignTop)
        scroll_layout.addLayout(self.relations_layout)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setMaximumHeight(400)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        content_layout.addWidget(scroll_area)

        add_button_layout = QHBoxLayout()
        add_button_layout.addStretch()
        self.add_button = QPushButton("Adicionar Linha")
        self.add_button.setFixedWidth(150)
        self.add_button.clicked.connect(self.add_relation_row)
        add_button_layout.addWidget(self.add_button)
        content_layout.addLayout(add_button_layout)

        group_layout = QVBoxLayout()
        group_layout.addWidget(content_widget)
        self.group_box.setLayout(group_layout)

        main_layout.addWidget(self.group_box)
        self.setLayout(main_layout)

    def add_relation_row(self, data: Optional[DriversVehiclesRelation] = None) -> None:
        new_row = DriversVehiclesRelationRowWidget()
        new_row.remove_requested.connect(self.remove_relation_row)
        self.relations_layout.addWidget(new_row)
        self.relation_rows.append(new_row)
        if data:
            new_row.set_data(data)

    def remove_relation_row(self, row: DriversVehiclesRelationRowWidget) -> None:
        if row in self.relation_rows:
            self.relations_layout.removeWidget(row)
            self.relation_rows.remove(row)
            row.deleteLater()

        if len(self.relation_rows) == 0:
            self.add_relation_row()

    def get_relations(self) -> List[DriversVehiclesRelation]:
        relations = []
        for index, row in enumerate(self.relation_rows):
            relation = row.get_data(index)
            if relation:
                relations.append(relation)
        return relations

    def set_relations(self, relations: List[DriversVehiclesRelation]) -> None:
        for row in self.relation_rows[:]:
            self.relations_layout.removeWidget(row)
            self.relation_rows.remove(row)
            row.deleteLater()

        self.relations = relations

        if not relations:
            self.add_relation_row()
        else:
            for relation in relations:
                self.add_relation_row(relation)
