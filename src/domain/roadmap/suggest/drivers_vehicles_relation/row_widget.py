from typing import Optional

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QCheckBox, QHBoxLayout, QPushButton, QWidget

from domain.driver.field.active_drivers_combo_box import ActiveDriversComboBox
from domain.roadmap.suggest.drivers_vehicles_relation.model import DriversVehiclesRelation
from domain.vehicle.field.active_vehicles_combo_box import ActiveVehiclesComboBox


class DriversVehiclesRelationRowWidget(QWidget):
    remove_requested = Signal(object)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self) -> None:
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        self.driver_field = ActiveDriversComboBox()
        layout.addWidget(self.driver_field, 5)

        self.vehicle_field = ActiveVehiclesComboBox()
        layout.addWidget(self.vehicle_field, 5)

        self.on_call_driver_field = QCheckBox()
        layout.addWidget(self.on_call_driver_field, 2)

        self.remove_button = QPushButton("Remover Linha")
        self.remove_button.clicked.connect(lambda: self.remove_requested.emit(self))
        layout.addWidget(self.remove_button, 2)

        self.setLayout(layout)

    def get_data(self, index: int) -> Optional[DriversVehiclesRelation]:
        driver = self.driver_field.get_current_data()
        if not driver:
            raise ValueError(f"Selecione um motorista na linha {index + 1}")

        vehicle = self.vehicle_field.get_current_data()
        if not vehicle:
            raise ValueError(f"Selecione um veículo na linha {index + 1}")

        return DriversVehiclesRelation(
            driver=driver,
            vehicle=vehicle,
            on_call_driver=self.on_call_driver_field.isChecked(),
        )

    def set_data(self, relation: DriversVehiclesRelation) -> None:
        self.driver_field.setCurrentIndexByData(relation.driver)
        self.vehicle_field.setCurrentIndexByData(relation.vehicle)
        self.on_call_driver_field.setChecked(relation.on_call_driver)
