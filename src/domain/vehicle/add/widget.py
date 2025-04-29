from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import QFormLayout, QLabel, QLayout, QLineEdit

from common.gui.field.combo_box import ComboBox
from common.gui.field.license_plate_line_edit import LicensePlateLineEdit
from common.gui.widget.base_add_widget import BaseAddWidget
from domain.driver.model import Driver
from domain.vehicle.model import Vehicle


class VehicleAddWidget(BaseAddWidget):
    def __init__(self, parent=None):
        super().__init__(
            model_class=Vehicle,
            width=300,
            height=150,
            parent=parent,
        )

    def _create_form_fields(self) -> QLayout:
        layout = QFormLayout()

        self.license_plate_field = LicensePlateLineEdit()
        layout.addRow(QLabel("Placa:"), self.license_plate_field)

        self.description_field = QLineEdit()
        layout.addRow(QLabel("Descrição:"), self.description_field)

        self.capacity_field = QLineEdit()
        self.capacity_field.setValidator(QIntValidator())
        layout.addRow(QLabel("Capacidade:"), self.capacity_field)

        self.default_driver_combo_box = ComboBox(model_class=Driver)
        layout.addRow(QLabel("Motorista Padrão:"), self.default_driver_combo_box)

        return layout
