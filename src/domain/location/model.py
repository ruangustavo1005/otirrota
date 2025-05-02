from sqlalchemy import Column, String

from common.model.base_model import BaseModel
from common.model.column_types.point import Coordinate, Point


class Location(BaseModel):
    description = Column(String(), nullable=False, info={"title": "Descrição"})
    coordinates = Column(Point, nullable=False, info={"list": False})

    def __init__(self, description: str = None, coordinates: Coordinate = None):
        super().__init__()
        self.description = description
        self.coordinates = coordinates

    def get_description(self) -> str:
        return self.description

    @classmethod
    def get_static_description(cls) -> str:
        return "Localização"
