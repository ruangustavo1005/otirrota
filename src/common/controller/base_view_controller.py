from abc import abstractmethod
from typing import Generic

from common.controller.base_crud_controller import BaseCRUDController, ModelType
from common.controller.base_list_controller import BaseListController
from common.gui.widget.base_view_widget import BaseViewWidget


class BaseViewController(BaseCRUDController[ModelType], Generic[ModelType]):
    _widget: BaseViewWidget[ModelType]

    def __init__(
        self, entity: ModelType, caller: BaseListController | None = None
    ) -> None:
        self._entity = entity
        super().__init__(caller)
        self._populate_view(entity)
        self._widget.submit_button.hide()

    @abstractmethod
    def _populate_view(self, entity: ModelType) -> None:
        raise NotImplementedError()

    @abstractmethod
    def _get_widget_instance(self) -> BaseViewWidget[ModelType]:
        raise NotImplementedError()

    def execute_action(self) -> None:
        pass
