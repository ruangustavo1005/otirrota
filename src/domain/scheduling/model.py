from __future__ import annotations

from datetime import datetime, time  # noqa: F401
from typing import TYPE_CHECKING, Any, List, Optional

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Time
from sqlalchemy.orm import Mapped, relationship

from common.model.base_model import BaseModel
from domain.location.model import Location
from domain.patient.model import Patient
from domain.purpose.model import Purpose

if TYPE_CHECKING:
    from domain.companion.model import Companion


class Scheduling(BaseModel):
    datetime = Column(  # noqa: F811
        DateTime, nullable=False, info={"title": "Data e Hora"}
    )
    location_id = Column(
        Integer,
        ForeignKey("location.id", ondelete="RESTRICT"),
        nullable=False,
        info={"title": "Localização"},
    )
    purpose_id = Column(
        Integer,
        ForeignKey("purpose.id", ondelete="RESTRICT"),
        nullable=False,
        info={"title": "Finalidade"},
    )
    average_duration = Column(Time, nullable=False, info={"title": "Duração Estimada"})
    patient_id = Column(
        Integer,
        ForeignKey("patient.id", ondelete="RESTRICT"),
        nullable=True,
        info={"title": "Paciente"},
    )
    sensitive_patient = Column(
        Boolean, nullable=True, info={"title": "Paciente Sensível?"}
    )
    description = Column(String, nullable=True, info={"list": False})

    location: Mapped[Location] = relationship("Location", foreign_keys=[location_id])
    purpose: Mapped[Purpose] = relationship("Purpose", foreign_keys=[purpose_id])
    patient: Mapped[Optional[Patient]] = relationship("Patient", foreign_keys=[patient_id])
    companions: Mapped[Optional[List["Companion"]]] = relationship(
        "Companion", back_populates="scheduling", cascade="all, delete-orphan"
    )

    def __init__(
        self,
        datetime: "datetime" = None,
        location_id: int = None,
        purpose_id: int = None,
        average_duration: time = None,
        patient_id: int = None,
        sensitive_patient: bool = False,
        description: str = None,
    ):
        super().__init__()
        self.datetime = datetime
        self.location_id = location_id
        self.purpose_id = purpose_id
        self.average_duration = average_duration
        self.patient_id = patient_id
        self.sensitive_patient = sensitive_patient
        self.description = description

    def format_for_table(self) -> List[Any]:
        result = super().format_for_table()

        result[1] = self.location.get_description()
        result[2] = self.purpose.get_description()
        result[4] = self.patient.get_description() if self.patient else ""

        if self.companions:
            result[4] += f" (+{len(self.companions)})"

        return result

    def get_description(self) -> str:
        datetime_str = self.datetime.strftime("%d/%m/%Y %H:%M")
        patient = self.patient.get_description() if self.patient else ""
        if self.companions:
            patient += f" (+{len(self.companions)})"
        location = self.location.get_description()
        purpose = self.purpose.get_description()

        return f"[{datetime_str}] {location} ({purpose}) {patient}".strip()

    @classmethod
    def get_static_description(cls) -> str:
        return "Agendamento"
