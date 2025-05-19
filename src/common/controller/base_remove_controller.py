import re
from importlib import import_module
from typing import Generic

from PySide6.QtWidgets import QMessageBox
from sqlalchemy.exc import IntegrityError

from common.controller.base_crud_controller import BaseCRUDController, ModelType
from common.controller.base_entity_controller import BaseEntityController
from common.controller.base_list_controller import BaseListController
from common.gui.widget.base_entity_widget import BaseEntityWidget
from common.model.base_model import BaseModel


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
        except IntegrityError as e:
            self._handle_integrity_error(e)
            return False
        except Exception as e:
            self._handle_remove_exception(e)
            return False

    def _handle_integrity_error(self, e: IntegrityError) -> None:
        error_message = str(e)

        match = re.search(
            r'foreign key constraint "(\w+)_(\w+)_id_fkey"',
            error_message,
            re.IGNORECASE,
        )

        if match:
            relation_name = match.group(1)
            if relation_name == self._model_class.__tablename__:
                relation_name = match.group(2)

            try:
                module_path = f"domain.{relation_name}.model"
                module = import_module(module_path)
                relation_class = getattr(module, relation_name.capitalize())

                if relation_class and issubclass(relation_class, BaseModel):
                    BaseEntityWidget.show_warning_pop_up(
                        "Atenção",
                        f"Não é possível excluir este(a) {self._model_class.get_static_description()}",
                        f"Existem registros de {relation_class.get_static_description()} vinculados que impedem a exclusão.",
                    )
                return
            except (ImportError, AttributeError):
                pass

        BaseEntityWidget.show_error_pop_up(
            "Erro",
            f"Não é possível excluir este(a) {self._model_class.get_static_description()}",
            "Existem registros vinculados que impedem a exclusão.",
        )

    def _handle_remove_exception(self, e: Exception) -> None:
        BaseEntityWidget.show_error_pop_up(
            "Erro",
            f"Erro ao excluir o(a) {self._model_class.get_static_description()}",
            "Por favor, entre em contato com o suporte",
        )
