from abc import abstractmethod
from typing import Generic

from common.controller.base_crud_controller import BaseCRUDController, ModelType
from common.controller.base_list_controller import BaseListController
from common.gui.widget.base_view_widget import BaseViewWidget
from db import Database


class BaseViewController(BaseCRUDController[ModelType], Generic[ModelType]):
    _widget: BaseViewWidget[ModelType]
    _data_id: int
    _entity: ModelType = None

    def __init__(self, data_id: int, caller: BaseListController | None = None) -> None:
        self._data_id = data_id
        super().__init__(caller)
        self._load_data()
        self._widget.submit_button.hide()

    def _load_data(self) -> None:
        with Database.session_scope() as session:
            self._entity = self._model_class.get_by_id(self._data_id, session)
            self._populate_view(self._entity)

    @abstractmethod
    def _populate_view(self, entity: ModelType) -> None:
        raise NotImplementedError()

    @abstractmethod
    def _get_widget_instance(self) -> BaseViewWidget[ModelType]:
        raise NotImplementedError()

    def execute_action(self) -> None:
        pass
