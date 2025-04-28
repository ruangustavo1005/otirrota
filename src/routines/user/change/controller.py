import hashlib
from typing import Any, Dict, Optional, Type

from sqlalchemy.exc import IntegrityError

from common.controller.base_change_controller import BaseChangeController
from common.controller.base_entity_controller import ModelType
from common.gui.widget.base_change_widget import BaseChangeWidget
from routines.user.change.widget import UserChangeWidget
from routines.user.model import User


class UserChangeController(BaseChangeController[User]):
    _widget: UserChangeWidget

    def _populate_form(self, entity: User) -> None:
        self._widget.name_field.setText(entity.name)
        self._widget.user_name_field.setText(entity.user_name)
        self._widget.active_field.setChecked(entity.active)

    def _get_model_updates(self) -> Optional[Dict[str, Any]]:
        name = self._widget.name_field.text()
        if not name:
            self._widget.show_info_pop_up("Atenção", "O nome é obrigatório")
            return None

        user_name = self._widget.user_name_field.text()
        if not user_name:
            self._widget.show_info_pop_up("Atenção", "O login é obrigatório")
            return None

        password = self._widget.password_field.text()
        confirm_password = self._widget.confirm_password_field.text()
        if password and not confirm_password or confirm_password and not password:
            self._widget.show_info_pop_up(
                "Atenção", "Preencha a senha e a confirmação para alterar a senha"
            )
            return None

        if password and confirm_password:
            if password != confirm_password:
                self._widget.show_info_pop_up("Atenção", "As senhas não conferem")
                return None

        updates = {
            "name": name.strip(),
            "user_name": user_name.strip(),
            "active": self._widget.active_field.isChecked(),
        }

        if password:
            updates["password"] = hashlib.md5(password.strip().encode()).hexdigest()

        return updates

    def _handle_change_exception(self, e: Exception) -> None:
        if isinstance(e, IntegrityError):
            self._widget.show_warning_pop_up(
                "Atenção",
                f'O login "{self._widget.user_name_field.text()}" já está em uso',
            )

    def _get_widget_instance(self) -> BaseChangeWidget:
        return UserChangeWidget()

    def _get_model_class(self) -> Type[ModelType]:
        return User
