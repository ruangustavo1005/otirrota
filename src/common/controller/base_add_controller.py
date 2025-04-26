from abc import abstractmethod
from typing import Generic, Optional

from common.controller.base_crud_controller import BaseCRUDController
from common.controller.base_controller import ModelType
from common.gui.widget.base_add_widget import BaseAddWidget


class BaseAddController(BaseCRUDController[ModelType], Generic[ModelType]):
    _widget: BaseAddWidget[ModelType]

    @abstractmethod
    def _get_widget_instance(self) -> BaseAddWidget[ModelType]:
        raise NotImplementedError()

    @abstractmethod
    def _get_populated_model(self) -> Optional[ModelType]:
        raise NotImplementedError()

    def execute_action(self) -> None:
        try:
            if model := self._get_populated_model():
                model.save()
                self._widget.show_info_pop_up(
                    "Sucesso",
                    f"{self._model_class.get_static_description()} criado(a) com sucesso",
                )
                self._caller.update_table_data()
                self._widget.close()
        except Exception:
            self._widget.show_error_pop_up(
                "Erro",
                f"Erro ao criar o(a) {self._model_class.get_static_description()}",
                "Por favor, entre em contato com o suporte",
            )