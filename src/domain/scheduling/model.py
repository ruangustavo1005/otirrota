from __future__ import annotations

from datetime import datetime, time  # noqa: F401
from typing import TYPE_CHECKING, Any, List, Optional

from dateutil.relativedelta import relativedelta
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Time, or_
from sqlalchemy.orm import Mapped, relationship

from common.model.base_model import BaseModel
from domain.location.model import Location
from domain.patient.model import Patient
from domain.purpose.model import Purpose

if TYPE_CHECKING:
    from domain.companion.model import Companion
    from domain.roadmap.model import Roadmap


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
    roadmap_id = Column(
        Integer,
        ForeignKey("roadmap.id", ondelete="SET NULL"),
        nullable=True,
        info={"list": False},
    )
    description = Column(String, nullable=True, info={"list": False})

    location: Mapped[Location] = relationship("Location", foreign_keys=[location_id])
    purpose: Mapped[Purpose] = relationship("Purpose", foreign_keys=[purpose_id])
    patient: Mapped[Optional[Patient]] = relationship(
        "Patient", foreign_keys=[patient_id]
    )
    roadmap: Mapped[Optional["Roadmap"]] = relationship(
        "Roadmap", foreign_keys=[roadmap_id], back_populates="schedulings"
    )
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
        roadmap_id: int = None,
        description: str = None,
    ):
        super().__init__()
        self.datetime = datetime
        self.location_id = location_id
        self.purpose_id = purpose_id
        self.average_duration = average_duration
        self.patient_id = patient_id
        self.sensitive_patient = sensitive_patient
        self.roadmap_id = roadmap_id
        self.description = description

    def get_roadmap_exists(self) -> bool:
        return self.roadmap is not None

    @classmethod
    def list_for_combo_box(
        cls,
        roadmap_id: int = None,
        date: datetime = None,
        ids_ignore: List[int] = None,
        **kwargs: Any,
    ) -> List[Scheduling]:
        if roadmap_id:
            query = cls.query().filter(or_(cls.roadmap_id.is_(None), cls.roadmap_id == roadmap_id))
        else:
            query = cls.query().filter(cls.roadmap_id.is_(None))

        if date:
            start_datetime = datetime(
                year=date.year,
                month=date.month,
                day=date.day,
                hour=0,
                minute=0,
                second=0,
            )
            end_datetime = start_datetime + relativedelta(days=1)
            query = (
                query.filter(cls.datetime >= start_datetime)
                .filter(cls.datetime <= end_datetime)
                .order_by(cls.id)
            )
            if ids_ignore:
                query = query.filter(cls.id.notin_(ids_ignore))

        return [record for record in query.order_by(cls.datetime)]

    def format_for_table(self) -> List[Any]:
        result = super().format_for_table()

        if self.companions:
            result[4] += f" (+{len(self.companions)})"

        return result

    @classmethod
    def _get_model_listable_columns(cls) -> List[Column]:
        return super()._get_model_listable_columns() + [
            Column(
                name="roadmap_exists",
                type_=Boolean,
                info={"title": "Possui Roteiro?"},
            ),
        ]

    def get_description(self) -> str:
        datetime_str = self.datetime.strftime("%d/%m/%Y %H:%M")
        patient = self.patient.get_description() if self.patient else ""
        if self.companions:
            patient += f" (+{len(self.companions)})"
        location = self.location.get_description()
        purpose = self.purpose.get_description()

        return f"[{datetime_str}] {location} ({purpose}) {patient}".strip()

    def get_passenger_count(self) -> int:
        return (
            1 + (len(self.companions) if self.companions else 0) if self.patient else 0
        )

    @classmethod
    def get_static_description(cls) -> str:
        return "Agendamento"
