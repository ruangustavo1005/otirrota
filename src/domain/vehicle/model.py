from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Optional

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, relationship

from common.model.base_model import BaseModel
from common.utils.string import StringUtils

if TYPE_CHECKING:
    from domain.driver.model import Driver


class Vehicle(BaseModel):
    license_plate = Column(String(7), nullable=False, info={"title": "Placa"})
    description = Column(String, nullable=False, info={"title": "Descrição"})
    capacity = Column(Integer, nullable=False, info={"title": "Capacidade"})
    default_driver_id = Column(
        Integer,
        ForeignKey("driver.id", ondelete="SET NULL"),
        nullable=True,
        info={"title": "Motorista Padrão"},
    )
    active = Column(Boolean, nullable=False, default=True, info={"title": "Ativo?"})

    default_driver: Mapped[Optional["Driver"]] = relationship(
        "Driver", foreign_keys=[default_driver_id]
    )

    def __init__(
        self,
        license_plate: str = None,
        description: str = None,
        capacity: int = None,
        default_driver_id: int = None,
        active: bool = True,
    ):
        super().__init__()
        self.license_plate = license_plate
        self.description = description
        self.capacity = capacity
        self.default_driver_id = default_driver_id
        self.active = active

    def format_license_plate(self) -> str:
        return StringUtils.format_license_plate(self.license_plate)

    def format_for_table(self) -> List[Any]:
        result = super().format_for_table()

        result[1] = self.format_license_plate()

        if self.default_driver:
            result[4] = self.default_driver.get_description()

        return result

    def get_combo_box_description(self) -> str:
        return f"{self.get_description()}{f' ({self.default_driver.name})' if self.default_driver else ''}"

    def get_description(self) -> str:
        prefix = ""
        if not self.active:
            prefix = "(Inativo) "
        return f"{prefix}{self.format_license_plate()} - {self.description}"

    @classmethod
    def get_static_description(cls) -> str:
        return "Veículo"
