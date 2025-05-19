from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Optional

if TYPE_CHECKING:
    from domain.vehicle.model import Vehicle

from sqlalchemy import Boolean, Column, Select, String
from sqlalchemy.orm import Mapped, relationship

from common.model.base_model import BaseModel
from common.utils.string import StringUtils


class Driver(BaseModel):
    name = Column(String(), nullable=False, info={"title": "Nome"})
    cpf = Column(String(11), nullable=False, info={"title": "CPF"})
    registration_number = Column(String, nullable=False, info={"title": "Registro"})
    active = Column(Boolean, nullable=False, default=True, info={"title": "Ativo?"})

    default_from_vehicle: Mapped[Optional["Vehicle"]] = relationship(
        "Vehicle",
        foreign_keys="Vehicle.default_driver_id",
        primaryjoin="and_(Driver.id==Vehicle.default_driver_id, Vehicle.active==True)",
        uselist=False,
        viewonly=True,
    )

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

    def format_cpf(self) -> Optional[str]:
        return StringUtils.format_cpf(self.cpf)

    def format_for_table(self) -> List[Any]:
        result = super().format_for_table()

        result[1] = self.format_cpf()

        return result

    @classmethod
    def _get_model_listable_columns(cls) -> List[Column]:
        return super()._get_model_listable_columns() + [
            Column(
                name="default_from_vehicle",
                type_=String,
                info={"title": "Veículo Padrão"},
            )
        ]

    def get_description(self) -> str:
        prefix = ""
        if not self.active:
            prefix = "(Inativo) "
        return f"{prefix}{self.name}"

    @classmethod
    def get_static_description(cls) -> str:
        return "Motorista"

    @classmethod
    def apply_text_search_filter(cls, query: Select, search_text: str) -> Select:
        text_parts = search_text.split(" ")
        for text_part in text_parts:
            query = query.filter(cls.name.ilike(f"%{text_part}%"))
        return query
