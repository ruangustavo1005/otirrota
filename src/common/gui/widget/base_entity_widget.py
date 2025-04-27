from typing import Generic, Type, TypeVar

from PySide6.QtCore import Qt

from common.gui.widget.base_widget import BaseWidget
from common.model.base_model import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)


class BaseEntityWidget(BaseWidget, Generic[ModelType]):
    model_class: Type[ModelType]

    def __init__(
        self,
        model_class: Type[ModelType],
        title: str,
        width: int,
        height: int,
        parent=None,
        flags=Qt.WindowFlags(),
    ):
        self.model_class = model_class
        super().__init__(title, width, height, parent, flags)
