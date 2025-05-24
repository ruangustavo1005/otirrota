from typing import Optional, Tuple

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QCheckBox, QHBoxLayout, QWidget

from domain.driver.field.active_drivers_combo_box import ActiveDriversComboBox
from domain.driver.model import Driver


class DriversRelationRowWidget(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self) -> None:
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        use_checkbox_container = QWidget()
        use_checkbox_layout = QHBoxLayout(use_checkbox_container)
        use_checkbox_layout.setContentsMargins(0, 0, 0, 0)
        use_checkbox_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.use_field = QCheckBox()
        self.use_field.setChecked(True)
        self.use_field.stateChanged.connect(self.on_use_field_changed)
        use_checkbox_layout.addWidget(self.use_field)

        layout.addWidget(use_checkbox_container, 1)

        self.driver_field = ActiveDriversComboBox()
        self.driver_field.set_read_only(True)
        layout.addWidget(self.driver_field, 7)

        on_call_checkbox_container = QWidget()
        on_call_checkbox_layout = QHBoxLayout(on_call_checkbox_container)
        on_call_checkbox_layout.setContentsMargins(0, 0, 0, 0)
        on_call_checkbox_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.on_call_driver_field = QCheckBox()
        on_call_checkbox_layout.addWidget(self.on_call_driver_field)

        layout.addWidget(on_call_checkbox_container, 2)

        self.setLayout(layout)

    def on_use_field_changed(self, state: int) -> None:
        self.driver_field.setEnabled(state == Qt.CheckState.Checked.value)

    def get_data(self) -> Optional[Tuple[Driver, bool]]:
        if self.use_field.isChecked():
            return (
                self.driver_field.get_current_data(),
                self.on_call_driver_field.isChecked(),
            )
        return None

    def set_data(self, driver: Driver) -> None:
        self.driver_field.setCurrentIndexByData(driver)
