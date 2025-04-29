from PySide6.QtCore import Qt
from PySide6.QtWidgets import QCheckBox, QHBoxLayout, QLabel, QLineEdit

from common.gui.field.license_plate_line_edit import LicensePlateLineEdit
from common.gui.widget.base_list_widget import BaseListWidget
from domain.vehicle.model import Vehicle


class VehicleListWidget(BaseListWidget[Vehicle]):
    def __init__(
        self,
        parent=None,
    ):
        super().__init__(
            model_class=Vehicle,
            width=1000,
            height=738,
            parent=parent,
        )

    def _create_filter_fields(self, filter_area_layout: QHBoxLayout) -> None:
        license_plate_label = QLabel("Placa:")
        license_plate_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        license_plate_label.setFixedWidth(40)
        filter_area_layout.addWidget(license_plate_label)

        self.license_plate_filter = LicensePlateLineEdit()
        self.license_plate_filter.setFixedWidth(100)
        self.license_plate_filter.returnPressed.connect(self.update_button.click)
        filter_area_layout.addWidget(self.license_plate_filter)

        description_label = QLabel("Descrição:")
        description_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        description_label.setFixedWidth(60)
        filter_area_layout.addWidget(description_label)

        self.description_filter = QLineEdit()
        self.description_filter.setFixedWidth(120)
        self.description_filter.returnPressed.connect(self.update_button.click)
        filter_area_layout.addWidget(self.description_filter)

        active_label = QLabel("Ativo?")
        active_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        active_label.setFixedWidth(40)
        filter_area_layout.addWidget(active_label)

        self.active_filter = QCheckBox()
        self.active_filter.setChecked(True)
        filter_area_layout.addWidget(self.active_filter)

    def _create_actions_area(self) -> QHBoxLayout:
        layout = super()._create_actions_area()
        self.view_button.setVisible(False)
        return layout
