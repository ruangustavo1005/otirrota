from typing import Generic

from PySide6.QtWidgets import QMessageBox

from common.controller.base_crud_controller import BaseCRUDController, ModelType
from common.controller.base_list_controller import BaseListController
from db import Database


class BaseRemoveController(BaseCRUDController[ModelType], Generic[ModelType]):
    _data_id: int

    def __init__(self, data_id: int, caller: BaseListController | None = None) -> None:
        self._data_id = data_id
        self._caller = caller
        self._model_class = self._get_model_class()

    def _get_widget_instance(self):
        pass

    def show(self) -> None:
        pass

    def execute_action(self) -> None:
        model_description = self._model_class.get_static_description()
        option = self._widget.show_question_pop_up(
            "Atenção",
            f"Tem certeza que deseja excluir o(a) {model_description}?",
            "Esta ação não pode ser revertida.",
        )
        if option == QMessageBox.StandardButton.Yes:
            with Database.session_scope() as session:
                try:
                    entity = self._model_class.get_by_id(self._data_id, session)
                    if entity:
                        entity.delete(session)
                        if self._caller:
                            self._caller.update_table_data()
                        self._widget.show_info_pop_up(
                            "Sucesso",
                            f"{model_description} removido(a) com sucesso!",
                        )
                except Exception as e:
                    self._widget.show_error_pop_up(
                        "Erro",
                        f"Erro ao excluir o(a) {model_description}",
                        "Por favor, entre em contato com o suporte",
                    )
