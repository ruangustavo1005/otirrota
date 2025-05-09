from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, relationship

from common.model.base_model import BaseModel
from common.utils.string import StringUtils

if TYPE_CHECKING:
    from domain.scheduling.model import Scheduling


class Companion(BaseModel):
    scheduling_id = Column(
        Integer,
        ForeignKey("scheduling.id", ondelete="CASCADE"),
        nullable=False,
        info={"title": "Agendamento"},
    )
    name = Column(String, nullable=False, info={"title": "Nome"})
    cpf = Column(String(11), nullable=True, info={"title": "CPF"})
    phone = Column(String(11), nullable=True, info={"title": "Telefone"})

    scheduling: Mapped["Scheduling"] = relationship(
        "Scheduling", back_populates="companions"
    )

    def __init__(
        self,
        scheduling_id: int = None,
        name: str = None,
        cpf: str = None,
        phone: str = None,
    ):
        super().__init__()
        self.scheduling_id = scheduling_id
        self.name = name
        self.cpf = cpf
        self.phone = phone

    def format_cpf(self) -> Optional[str]:
        return StringUtils.format_cpf(self.cpf)

    def format_phone(self) -> Optional[str]:
        return StringUtils.format_phone(self.phone)

    def get_description(self) -> str:
        return self.name

    @classmethod
    def get_static_description(cls) -> str:
        return "Acompanhante"
