from sqlalchemy import Column, Float, Integer, String

from common.model.base_model import BaseModel
from common.model.column_types.point import Coordinate, Point


class Config(BaseModel):
    department_name = Column(String(), nullable=True)
    body_name = Column(String(), nullable=True)
    eplison = Column(Float, nullable=True)
    minpts = Column(Integer, nullable=True)
    distance_matrix_api_key = Column(String(), nullable=True)
    departure_coordinates = Column(Point, nullable=True)

    def __init__(
        self,
        department_name: str = None,
        body_name: str = None,
        eplison: float = None,
        minpts: int = None,
        distance_matrix_api_key: str = None,
        departure_coordinates: Coordinate = None,
    ):
        super().__init__()
        self.department_name = department_name
        self.body_name = body_name
        self.eplison = eplison
        self.minpts = minpts
        self.distance_matrix_api_key = distance_matrix_api_key
        self.departure_coordinates = departure_coordinates

    def get_description(self) -> str:
        return self.get_static_description()

    @classmethod
    def get_static_description(cls) -> str:
        return "Configurações"

    @classmethod
    def get_config(cls) -> "Config":
        return Config.get_by_id(1)
