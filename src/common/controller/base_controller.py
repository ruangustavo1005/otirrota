from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, Type, TypeVar

from common.gui.widget.base_widget import BaseWidget
from common.model.base_model import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)


class BaseController(ABC, Generic[ModelType]):
    _widget: BaseWidget[ModelType]
    _model_class: Type[ModelType]
    _caller: BaseController

    def __init__(self, caller: BaseController | None = None) -> None:
        self._caller = caller
        self._widget = self._get_widget_instance()
        if not hasattr(self, "_model_class"):
            self._model_class = self._get_model_class()

    @abstractmethod
    def _get_widget_instance(self) -> BaseWidget[ModelType]:
        raise NotImplementedError()

    @abstractmethod
    def _get_model_class(self) -> Type[ModelType]:
        raise NotImplementedError()

    def show(self) -> None:
        self._widget.show()
