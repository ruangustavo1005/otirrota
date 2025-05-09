from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QLabel, QLineEdit

from common.gui.widget.base_list_widget import BaseListWidget
from domain.purpose.model import Purpose


class PurposeListWidget(BaseListWidget[Purpose]):
    def __init__(
        self,
        parent=None,
    ):
        super().__init__(
            model_class=Purpose,
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
        return layout
