from abc import abstractmethod
from typing import Any, Dict, Generic, Optional

from common.controller.base_controller import ModelType
from common.controller.base_crud_controller import BaseCRUDController
from common.controller.base_list_controller import BaseListController
from common.gui.widget.base_change_widget import BaseChangeWidget


class BaseChangeController(BaseCRUDController[ModelType], Generic[ModelType]):
    _widget: BaseChangeWidget[ModelType]

    def __init__(
        self, entity: ModelType, caller: BaseListController | None = None
    ) -> None:
        self._entity = entity
        super().__init__(caller)
        self._populate_form(self._entity)

    @abstractmethod
    def _populate_form(self, entity: ModelType) -> None:
        raise NotImplementedError()

    @abstractmethod
    def _get_model_updates(self) -> Optional[Dict[str, Any]]:
        raise NotImplementedError()

    def execute_action(self) -> None:
        try:
            if updates := self._get_model_updates():
                self._entity.update(**updates)
                self._widget.show_info_pop_up(
                    "Sucesso",
                    f"{self._model_class.get_static_description()} alterado(a) com sucesso",
                )
                self._caller.update_table_data()
                self._widget.close()
        except Exception as e:
            raise e
            self._widget.show_error_pop_up(
                "Erro",
                f"Erro ao alterar o(a) {self._model_class.get_static_description()}",
                "Por favor, entre em contato com o suporte",
            )

    @abstractmethod
    def _get_widget_instance(self) -> BaseChangeWidget[ModelType]:
        raise NotImplementedError()
