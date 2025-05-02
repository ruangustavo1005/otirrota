import sqlalchemy
from dataclasses import dataclass
from typing import Tuple, Union


@dataclass(eq=True, frozen=True, slots=True)
class Coordinate:
    latitude: float
    longitude: float


class Point(sqlalchemy.types.UserDefinedType):
    cache_ok = True

    def get_col_spec(self):
        return "POINT"

    def bind_expression(self, bindvalue):
        return sqlalchemy.func.POINT(bindvalue, type_=self)

    def bind_processor(self, dialect):
        def process(
            value: Union[Coordinate, Tuple[float, float], None],
        ) -> Union[str, None]:
            if value is None:
                return None

            if isinstance(value, tuple):
                value = Coordinate(*value)

            return f"({value.latitude},{value.longitude})"

        return process

    def result_processor(self, dialect, coltype):
        def process(value: str) -> Union[Coordinate, None]:
            if value is None:
                return None

            lat, lng = value.strip("()").split(",")

            return Coordinate(float(lat), float(lng))

        return process
