from sqlalchemy import Column, String

from common.model.base_model import BaseModel


class Purpose(BaseModel):
    description = Column(String(), nullable=False, info={"title": "Descrição"})

    def __init__(self, description: str = None):
        super().__init__()
        self.description = description

    def get_combo_box_description(self) -> str:
        return self.description

    def get_description(self) -> str:
        return self.description

    @classmethod
    def get_static_description(cls) -> str:
        return "Finalidade"
