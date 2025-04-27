from typing import Type

from common.controller.base_entity_controller import ModelType
from common.controller.base_remove_controller import BaseRemoveController
from common.gui.widget.base_widget import BaseWidget
from routines.user.model import User
from settings import Settings


class UserRemoveController(BaseRemoveController[User]):
    def _get_model_class(self) -> Type[ModelType]:
        return User

    def execute_action(self) -> None:
        if self._entity.id == Settings.get_logged_user().id:
            BaseWidget.show_warning_pop_up(
                "Atenção",
                "Você não pode excluir seu próprio usuário.",
            )
        else:
            super().execute_action()
