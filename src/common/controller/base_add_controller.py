from abc import abstractmethod
from typing import Generic

from common.controller.base_crud_controller import BaseCRUDController, ModelType
from common.gui.widget.base_add_widget import BaseAddWidget


class BaseAddController(BaseCRUDController[ModelType], Generic[ModelType]):
    _widget: BaseAddWidget[ModelType]

    @abstractmethod
    def _get_widget_instance(self) -> BaseAddWidget[ModelType]:
        raise NotImplementedError()
