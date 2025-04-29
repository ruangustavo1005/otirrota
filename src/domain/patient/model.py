from typing import Any, List

from sqlalchemy import Column, String

from common.model.base_model import BaseModel
from common.utils.string import StringUtils


class Patient(BaseModel):
    name = Column(String(), nullable=False, info={"title": "Nome"})
    cpf = Column(String(11), nullable=False, info={"title": "CPF"})
    phone = Column(String(11), nullable=True, info={"title": "Telefone"})

    def __init__(self, name: str = None, cpf: str = None, phone: str = None):
        super().__init__()
        self.name = name
        self.cpf = cpf
        self.phone = phone

    def format_cpf(self) -> str:
        return StringUtils.format_cpf(self.cpf)

    def format_phone(self) -> str:
        return StringUtils.format_phone(self.phone) if self.phone else ""

    def format_for_table(self) -> List[Any]:
        result = super().format_for_table()

        result[2] = self.format_cpf()
        result[3] = self.format_phone()

        return result

    def get_description(self) -> str:
        return self.name

    @classmethod
    def get_static_description(cls) -> str:
        return "Paciente"
