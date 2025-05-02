from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QPushButton

from common.gui.widget.base_list_widget import BaseListWidget
from domain.location.model import Location


class LocationListWidget(BaseListWidget[Location]):
    def __init__(
        self,
        parent=None,
    ):
        super().__init__(
            model_class=Location,
            width=1000,
            height=738,
            parent=parent,
        )

    def _create_filter_fields(self, filter_area_layout: QHBoxLayout) -> None:
        descricao_label = QLabel("Descrição:")
        descricao_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        descricao_label.setFixedWidth(60)
        filter_area_layout.addWidget(descricao_label)

        self.descricao_filter = QLineEdit()
        self.descricao_filter.setFixedWidth(100)
        self.descricao_filter.returnPressed.connect(self.update_button.click)
        filter_area_layout.addWidget(self.descricao_filter)

    def _create_actions_area(self) -> QHBoxLayout:
        layout = super()._create_actions_area()
        self.view_button.setVisible(False)
        self.open_maps_button = QPushButton("Abrir no Google Maps")
        self.open_maps_button.setFixedWidth(150)
        layout.addWidget(self.open_maps_button)
        return layout

    def enable_row_actions(self) -> None:
        super().enable_row_actions()
        self.open_maps_button.setDisabled(False)

    def disable_row_actions(self) -> None:
        super().disable_row_actions()
        self.open_maps_button.setDisabled(True)
