from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QCheckBox, QHBoxLayout, QWidget

from domain.vehicle.field.active_vehicles_combo_box import ActiveVehiclesComboBox
from domain.vehicle.model import Vehicle


class VehiclesRelationRowWidget(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self) -> None:
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        checkbox_container = QWidget()
        checkbox_layout = QHBoxLayout(checkbox_container)
        checkbox_layout.setContentsMargins(0, 0, 0, 0)
        checkbox_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.use_field = QCheckBox()
        self.use_field.setChecked(True)
        self.use_field.stateChanged.connect(self.on_use_field_changed)
        checkbox_layout.addWidget(self.use_field)

        layout.addWidget(checkbox_container, 1)

        self.vehicle_field = ActiveVehiclesComboBox()
        self.vehicle_field.set_read_only(True)
        layout.addWidget(self.vehicle_field, 9)

        self.setLayout(layout)

    def on_use_field_changed(self, state: int) -> None:
        self.vehicle_field.setEnabled(state == Qt.CheckState.Checked.value)

    def get_data(self) -> Optional[Vehicle]:
        if self.use_field.isChecked():
            return self.vehicle_field.get_current_data()
        return None

    def set_data(self, vehicle: Vehicle) -> None:
        self.vehicle_field.setCurrentIndexByData(vehicle)
