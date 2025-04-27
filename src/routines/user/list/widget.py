from PySide6.QtWidgets import QHBoxLayout, QLabel, QLineEdit

from common.gui.widget.base_list_widget import BaseListWidget
from routines.user.model import User


class UserListWidget(BaseListWidget[User]):
    def __init__(
        self,
        parent=None,
    ):
        super().__init__(
            model_class=User,
            width=1000,
            height=738,
            parent=parent,
        )

    def _create_filter_fields(self, filter_area_layout: QHBoxLayout) -> None:
        name_label = QLabel("Nome:")
        name_label.setFixedWidth(40)
        filter_area_layout.addWidget(name_label)

        self.name_filter = QLineEdit()
        self.name_filter.setFixedWidth(100)
        self.name_filter.returnPressed.connect(self.update_button.click)
        filter_area_layout.addWidget(self.name_filter)

    def _create_actions_area(self) -> QHBoxLayout:
        layout = super()._create_actions_area()
        self.view_button.setVisible(False)
        return layout
