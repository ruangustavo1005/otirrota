from typing import Any, List

from sqlalchemy import Boolean, Column, String

from common.model.base_model import BaseModel
from common.utils.string import StringUtils


class Driver(BaseModel):
    name = Column(String(), nullable=False, info={"title": "Nome"})
    cpf = Column(String(11), nullable=False, info={"title": "CPF"})
    registration_number = Column(String, nullable=False, info={"title": "Registro"})
    active = Column(Boolean, nullable=False, default=True, info={"title": "Ativo"})

    def __init__(
        self,
        name: str = None,
        cpf: str = None,
        registration_number: str = None,
        active: bool = True,
    ):
        super().__init__()
        self.name = name
        self.cpf = cpf
        self.registration_number = registration_number
        self.active = active

    def format_cpf(self) -> str:
        return StringUtils.format_cpf(self.cpf)

    def format_for_table(self) -> List[Any]:
        result = super().format_for_table()

        result[2] = self.format_cpf()

        return result

    def get_combo_box_description(self) -> str:
        return self.name

    def get_description(self) -> str:
        return self.name

    @classmethod
    def get_static_description(cls) -> str:
        return "Motorista"
