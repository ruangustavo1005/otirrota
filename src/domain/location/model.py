from sqlalchemy import Column, Select, String, and_

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

    @classmethod
    def apply_text_search_filter(cls, query: Select, search_text: str) -> Select:
        text_parts = search_text.split(" ")
        search_conditions = []
        for text_part in text_parts:
            text_part = text_part.strip()
            if not text_part:
                continue
            search_conditions.append(cls.description.ilike(f"%{text_part}%"))
        return query.filter(and_(*search_conditions))
