from abc import abstractmethod
from typing import Generic, Type

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QLayout, QPushButton, QVBoxLayout

from common.gui.widget.base_entity_widget import BaseEntityWidget, ModelType


class BaseCRUDWidget(BaseEntityWidget[ModelType], Generic[ModelType]):
    def __init__(
        self,
        model_class: Type[ModelType],
        title: str,
        width: int = 400,
        height: int = 400,
        parent=None,
        flags=Qt.WindowFlags(),
    ):
        super().__init__(model_class, title, width, height, parent, flags)

    def _init_ui(self) -> None:
        self.base_layout = QVBoxLayout()

        self.form_fields_layout = self._create_form_fields()
        self.base_layout.addLayout(self.form_fields_layout)

        self.actions_area_layout = self._create_actions_area()
        self.base_layout.addLayout(self.actions_area_layout)

        self.setLayout(self.base_layout)

    @abstractmethod
    def _create_form_fields(self) -> QLayout:
        raise NotImplementedError()

    def _create_actions_area(self) -> QHBoxLayout:
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.submit_button = QPushButton(self._get_submit_button_text())
        self.submit_button.setFixedWidth(100)
        layout.addWidget(self.submit_button)

        return layout

    def _get_submit_button_text(self):
        return "Confirmar"
