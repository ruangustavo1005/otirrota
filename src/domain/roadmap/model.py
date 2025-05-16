from __future__ import annotations

from datetime import date, datetime, time
from typing import TYPE_CHECKING, Any, List

from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, Time
from sqlalchemy.orm import Mapped, relationship

from common.model.base_model import BaseModel
from domain.driver.model import Driver
from domain.user.model import User
from domain.vehicle.model import Vehicle

if TYPE_CHECKING:
    from domain.scheduling.model import Scheduling


class Roadmap(BaseModel):
    driver_id = Column(
        Integer,
        ForeignKey("driver.id", ondelete="RESTRICT"),
        nullable=False,
        info={"title": "Motorista"},
    )
    vehicle_id = Column(
        Integer,
        ForeignKey("vehicle.id", ondelete="RESTRICT"),
        nullable=False,
        info={"title": "Veículo"},
    )
    departure = Column(DateTime, nullable=False, info={"list": False})
    arrival = Column(DateTime, nullable=False, info={"list": False})
    creation_user_id = Column(
        Integer,
        ForeignKey("user.id", ondelete="RESTRICT"),
        nullable=False,
        info={"list": False},
    )

    driver: Mapped[Driver] = relationship("Driver", foreign_keys=[driver_id])
    vehicle: Mapped[Vehicle] = relationship("Vehicle", foreign_keys=[vehicle_id])
    creation_user: Mapped[User] = relationship("User", foreign_keys=[creation_user_id])
    schedulings: Mapped[List["Scheduling"]] = relationship(
        "Scheduling", back_populates="roadmap", passive_deletes=True
    )

    def __init__(
        self,
        driver_id: int = None,
        vehicle_id: int = None,
        departure: datetime = None,
        arrival: datetime = None,
        creation_user_id: int = None,
    ):
        super().__init__()
        self.driver_id = driver_id
        self.vehicle_id = vehicle_id
        self.departure = departure
        self.arrival = arrival
        self.creation_user_id = creation_user_id

    def format_for_table(self) -> List[Any]:
        result = super().format_for_table()

        result[2] = self.format_value_for_table(
            date(self.departure.year, self.departure.month, self.departure.day)
        )
        result[3] = self.format_value_for_table(
            time(self.departure.hour, self.departure.minute)
        )
        result[4] = self.format_value_for_table(
            time(self.arrival.hour, self.arrival.minute)
        )

        return result

    @classmethod
    def _get_model_listable_columns(cls) -> List[Column]:
        return super()._get_model_listable_columns() + [
            Column(
                name="date",
                type_=Date,
                info={"title": "Data"},
            ),
            Column(
                name="departure_time",
                type_=Time,
                info={"title": "Saída"},
            ),
            Column(
                name="arrival_time",
                type_=Time,
                info={"title": "Chegada"},
            ),
            Column(
                name="passenger_count",
                type_=Integer,
                info={"title": "Qtd. Passageiros"},
            ),
        ]

    def get_description(self) -> str:
        departure_date_str = self.departure.strftime("%d/%m/%Y")
        departure_time_str = self.departure.strftime("%H:%M")
        arrival_time_str = self.arrival.strftime("%H:%M")
        driver_str = self.driver.get_description()
        vehicle_str = self.vehicle.get_description()
        passenger_count = self.get_passenger_count()

        return "[%s] %s à %s - %s, %s (%s passageiros)" % (
            departure_date_str,
            departure_time_str,
            arrival_time_str,
            driver_str,
            vehicle_str,
            passenger_count,
        )

    def get_passenger_count(self) -> int:
        return sum(scheduling.get_passenger_count() for scheduling in self.schedulings)

    @classmethod
    def get_static_description(cls) -> str:
        return "Roteiro"
