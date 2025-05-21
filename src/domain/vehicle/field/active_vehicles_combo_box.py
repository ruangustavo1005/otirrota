from typing import List

from common.gui.field.combo_box import ComboBox
from domain.vehicle.model import Vehicle


class ActiveVehiclesComboBox(ComboBox[Vehicle]):
    def __init__(self, default_none: bool = True, parent=None):
        super().__init__(parent, model_class=Vehicle, default_none=default_none)

    def _list_for_fill(self) -> List[Vehicle]:
        return Vehicle.query().filter(Vehicle.active == True).all()  # noqa: E712
