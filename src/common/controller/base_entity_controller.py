from __future__ import annotations

from abc import abstractmethod
from typing import Generic, Type, TypeVar

from common.controller.base_controller import BaseController
from common.gui.widget.base_entity_widget import BaseEntityWidget
from common.model.base_model import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)


class BaseEntityController(BaseController, Generic[ModelType]):
    _widget: BaseEntityWidget[ModelType]
    _model_class: Type[ModelType]

    def __init__(self, caller: BaseController | None = None) -> None:
        self._model_class = self._get_model_class()
        super().__init__(caller)

    @abstractmethod
    def _get_model_class(self) -> Type[ModelType]:
        raise NotImplementedError()

    def _get_widget_instance(self) -> BaseEntityWidget[ModelType]:
        raise NotImplementedError()

    def callee_finalized(self) -> None:
        pass
