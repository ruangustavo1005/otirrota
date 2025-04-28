from PySide6.QtWidgets import QFormLayout, QLabel, QLayout, QLineEdit

from common.gui.widget.base_change_widget import BaseChangeWidget
from domain.purpose.model import Purpose


class PurposeChangeWidget(BaseChangeWidget):
    def __init__(self, parent=None):
        super().__init__(
            model_class=Purpose,
            width=300,
            height=80,
            parent=parent,
        )

    def _create_form_fields(self) -> QLayout:
        layout = QFormLayout()

        self.description_field = QLineEdit()
        layout.addRow(QLabel("Descrição:"), self.description_field)

        return layout
