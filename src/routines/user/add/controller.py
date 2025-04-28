import hashlib
from typing import Optional, Type

from sqlalchemy.exc import IntegrityError

from common.controller.base_add_controller import BaseAddController
from common.controller.base_entity_controller import ModelType
from common.gui.widget.base_add_widget import BaseAddWidget
from routines.user.add.widget import UserAddWidget
from routines.user.model import User


class UserAddController(BaseAddController[User]):
    _widget: UserAddWidget

    def _get_populated_model(self) -> Optional[User]:
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
        if not password or not confirm_password:
            self._widget.show_info_pop_up("Atenção", "A senha é obrigatória")
            return None

        if password != confirm_password:
            self._widget.show_info_pop_up("Atenção", "As senhas não conferem")
            return None

        return User(
            name=name.strip(),
            user_name=user_name.strip(),
            password=hashlib.md5(password.strip().encode()).hexdigest(),
        )

    def _handle_add_exception(self, e: Exception) -> None:
        if isinstance(e, IntegrityError):
            self._widget.show_warning_pop_up(
                "Atenção",
                f'O login "{self._widget.user_name_field.text()}" já está em uso',
            )

    def _get_widget_instance(self) -> BaseAddWidget:
        return UserAddWidget()

    def _get_model_class(self) -> Type[ModelType]:
        return User
