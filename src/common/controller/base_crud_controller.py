from abc import abstractmethod
from typing import Generic

from common.controller.base_entity_controller import BaseEntityController, ModelType
from common.controller.base_list_controller import BaseListController
from common.gui.widget.base_crud_widget import BaseCRUDWidget


class BaseCRUDController(BaseEntityController[ModelType], Generic[ModelType]):
    _widget: BaseCRUDWidget[ModelType]

    def __init__(self, caller: BaseListController | None = None) -> None:
        super().__init__(caller)
        self._widget.submit_button.clicked.connect(self.execute_action)

    @abstractmethod
    def _get_widget_instance(self) -> BaseCRUDWidget[ModelType]:
        raise NotImplementedError()

    @abstractmethod
    def execute_action(self) -> None:
        raise NotImplementedError()
