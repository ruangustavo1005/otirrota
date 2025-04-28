from typing import Optional

from sqlalchemy import Boolean, Column, String

from common.model.base_model import BaseModel


class User(BaseModel):
    name = Column(String(), nullable=False, info={"title": "Nome"})
    user_name = Column(
        String(), nullable=False, unique=True, info={"title": "Nome de usuário"}
    )
    password = Column(
        String(32), nullable=False, info={"title": "Senha", "list": False}
    )
    active = Column(Boolean(), nullable=False, default=True, info={"title": "Ativo"})

    def __init__(
        self,
        name: str = None,
        user_name: str = None,
        password: str = None,
        active: bool = True,
    ):
        super().__init__()
        self.name = name
        self.user_name = user_name
        self.password = password
        self.active = active

    def get_combo_box_description(self) -> str:
        return self.name

    def get_description(self) -> str:
        return self.name

    @classmethod
    def get_static_description(cls) -> str:
        return "Usuário"

    @classmethod
    def is_login_valid(cls, user_name: str, password: str) -> Optional["User"]:
        query = cls.query().filter(cls.user_name == user_name, cls.password == password)
        user = query.one_or_none()
        return user if user and user.active else None
