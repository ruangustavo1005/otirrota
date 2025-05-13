from abc import abstractmethod
from typing import Any, Dict, Generic, Optional

from common.controller.base_crud_controller import BaseCRUDController
from common.controller.base_entity_controller import BaseEntityController, ModelType
from common.controller.base_list_controller import BaseListController
from common.gui.widget.base_change_widget import BaseChangeWidget
from db import Database


class BaseChangeController(BaseCRUDController[ModelType], Generic[ModelType]):
    _widget: BaseChangeWidget[ModelType]

    def __init__(
        self, entity: ModelType, caller: BaseListController | None = None
    ) -> None:
        self._entity_id = entity.id
        super().__init__(caller)
        self._populate_form(entity)

    @abstractmethod
    def _populate_form(self, entity: ModelType) -> None:
        raise NotImplementedError()

    @abstractmethod
    def _get_model_updates(self) -> Optional[Dict[str, Any]]:
        raise NotImplementedError()

    def execute_action(self) -> None:
        success = self._change()
        if success:
            if self._caller and isinstance(self._caller, BaseEntityController):
                print("callee_finalized")
                self._caller.callee_finalized()

    def _change(self) -> bool:
        with Database.session_scope() as session:
            try:
                if updates := self._get_model_updates():
                    entity = self._model_class.get_by_id(
                        self._entity_id, session=session
                    )
                    entity.update(session=session, **updates)
                    session.flush()
                    self._widget.show_info_pop_up(
                        "Sucesso",
                        f"{self._model_class.get_static_description()} alterado(a) com sucesso",
                    )
                    self._widget.close()
                    return True
            except Exception as e:
                self._handle_change_exception(e)
                return False

    def _handle_change_exception(self, e: Exception) -> None:
        self._widget.show_error_pop_up(
            "Erro",
            f"Erro ao alterar o(a) {self._model_class.get_static_description()}",
            "Por favor, entre em contato com o suporte",
        )

    @abstractmethod
    def _get_widget_instance(self) -> BaseChangeWidget[ModelType]:
        raise NotImplementedError()
