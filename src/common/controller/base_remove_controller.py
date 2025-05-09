from typing import Generic

from PySide6.QtWidgets import QMessageBox

from common.controller.base_crud_controller import BaseCRUDController, ModelType
from common.controller.base_entity_controller import BaseEntityController
from common.controller.base_list_controller import BaseListController
from common.gui.widget.base_entity_widget import BaseEntityWidget


class BaseRemoveController(BaseCRUDController[ModelType], Generic[ModelType]):
    def __init__(
        self, entity: ModelType, caller: BaseListController | None = None
    ) -> None:
        self._entity = entity
        self._caller = caller
        self._model_class = self._get_model_class()

    def _get_widget_instance(self):
        pass

    def show(self) -> None:
        self.execute_action()

    def execute_action(self) -> None:
        option = BaseEntityWidget.show_question_pop_up(
            "Atenção",
            f"Tem certeza que deseja excluir o(a) {self._model_class.get_static_description()}?",
            "Esta ação não pode ser revertida.",
        )
        if option == QMessageBox.StandardButton.Ok:
            success = self._remove()

            if success:
                if self._caller and isinstance(self._caller, BaseEntityController):
                    self._caller.callee_finalized()

    def _remove(self) -> bool:
        try:
            self._entity.delete()
            BaseEntityWidget.show_info_pop_up(
                "Sucesso",
                f"{self._model_class.get_static_description()} removido(a) com sucesso!",
            )
            return True
        except Exception as e:
            self._handle_remove_exception(e)
            return False

    def _handle_remove_exception(self, e: Exception) -> None:
        BaseEntityWidget.show_error_pop_up(
            "Erro",
            f"Erro ao excluir o(a) {self._model_class.get_static_description()}",
            "Por favor, entre em contato com o suporte",
        )
