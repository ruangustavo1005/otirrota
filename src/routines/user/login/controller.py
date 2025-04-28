import hashlib
from typing import Type

from common.controller.base_crud_controller import BaseCRUDController
from common.controller.base_entity_controller import ModelType
from routines.user.login.widget import LoginWidget
from routines.user.model import User
from settings import Settings


class LoginController(BaseCRUDController[User]):
    _widget: LoginWidget

    def _get_widget_instance(self) -> LoginWidget:
        return LoginWidget()

    def _get_model_class(self) -> Type[ModelType]:
        return User

    def execute_action(self) -> None:
        user_name = self._widget.user_name_field.text()
        password = self._widget.password_field.text()

        if user_name and password:
            user = User.is_login_valid(
                user_name, hashlib.md5(password.encode()).hexdigest()
            )
            if user:
                Settings.set_logged_user(user)
                self._caller.show()
                self._widget.close()
            else:
                self._widget.show_warning_pop_up(
                    "Atenção",
                    "Usuário ou senha inválidos",
                )
