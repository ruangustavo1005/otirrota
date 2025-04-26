from typing import Generic

from PySide6.QtWidgets import QMessageBox

from common.controller.base_crud_controller import BaseCRUDController, ModelType
from common.controller.base_list_controller import BaseListController
from common.gui.widget.base_widget import BaseWidget


class BaseRemoveController(BaseCRUDController[ModelType], Generic[ModelType]):
    def __init__(self, entity: ModelType, caller: BaseListController | None = None) -> None:
        self._entity = entity
        self._caller = caller
        self._model_class = self._get_model_class()

    def _get_widget_instance(self):
        pass

    def show(self) -> None:
        self.execute_action()

    def execute_action(self) -> None:
        model_description = self._model_class.get_static_description()
        option = BaseWidget.show_question_pop_up(
            "Atenção",
            f"Tem certeza que deseja excluir o(a) {model_description}?",
            "Esta ação não pode ser revertida.",
        )
        if option == QMessageBox.StandardButton.Ok:
            try:
                self._entity.delete()
                if self._caller:
                    self._caller.update_table_data()
                BaseWidget.show_info_pop_up(
                    "Sucesso",
                    f"{model_description} removido(a) com sucesso!",
                )
            except Exception as e:
                raise e
                BaseWidget.show_error_pop_up(
                    "Erro",
                    f"Erro ao excluir o(a) {model_description}",
                    "Por favor, entre em contato com o suporte",
                )
