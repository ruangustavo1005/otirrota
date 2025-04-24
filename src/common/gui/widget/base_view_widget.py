from typing import Generic, Type

from PySide6.QtCore import Qt

from common.gui.widget.base_crud_widget import BaseCRUDWidget, ModelType


class BaseViewWidget(BaseCRUDWidget[ModelType], Generic[ModelType]):
    def __init__(
        self,
        model_class: Type[ModelType],
        width: int = 400,
        height: int = 400,
        parent=None,
        flags=Qt.WindowFlags(),
    ):
        super().__init__(
            model_class=model_class,
            title=f"Visualizar {model_class.get_static_description()}",
            width=width,
            height=height,
            parent=parent,
            flags=flags,
        )
