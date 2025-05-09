from typing import Any, List

from sqlalchemy import Column, Select, String, and_

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
        return f"{self.name} - {self.format_cpf()}"

    @classmethod
    def get_static_description(cls) -> str:
        return "Paciente"

    @classmethod
    def apply_text_search_filter(cls, query: Select, search_text: str) -> Select:
        text_parts = search_text.split(" ")
        search_conditions = []
        for text_part in text_parts:
            text_part = text_part.strip()
            if not text_part:
                continue
            if text_part.isdigit():
                search_conditions.append(cls.cpf.ilike(f"%{text_part}%"))
            else:
                search_conditions.append(cls.name.ilike(f"%{text_part}%"))
        return query.filter(and_(*search_conditions))
