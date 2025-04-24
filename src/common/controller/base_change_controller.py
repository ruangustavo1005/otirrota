from abc import abstractmethod
from typing import Generic

from common.controller.base_crud_controller import BaseCRUDController, ModelType
from common.controller.base_list_controller import BaseListController
from common.gui.widget.base_change_widget import BaseChangeWidget
from db import Database


class BaseChangeController(BaseCRUDController[ModelType], Generic[ModelType]):
    _widget: BaseChangeWidget[ModelType]
    _data_id: int
    _entity: ModelType = None

    def __init__(self, data_id: int, caller: BaseListController | None = None) -> None:
        self._data_id = data_id
        super().__init__(caller)
        self._load_data()

    def _load_data(self) -> None:
        with Database.session_scope() as session:
            self._entity = self._model_class.get_by_id(self._data_id, session)
            self._populate_form(self._entity)

    @abstractmethod
    def _populate_form(self, entity: ModelType) -> None:
        raise NotImplementedError()

    @abstractmethod
    def _get_widget_instance(self) -> BaseChangeWidget[ModelType]:
        raise NotImplementedError()
