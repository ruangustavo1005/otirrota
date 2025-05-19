from typing import List

from common.gui.field.combo_box import ComboBox
from domain.driver.model import Driver
from domain.vehicle.model import Vehicle


class DriversWithoutVehicleComboBox(ComboBox[Driver]):
    def __init__(self, default_none: bool = True, parent=None):
        super().__init__(parent, model_class=Driver, default_none=default_none)

    def _list_for_fill(self) -> List[Driver]:
        return (
            Driver.query()
            .filter(
                Driver.active == True,  # noqa: E712
                ~Driver.id.in_(
                    Vehicle.query()
                    .filter(Vehicle.active == True)  # noqa: E712
                    .with_entities(Vehicle.default_driver_id)
                    .filter(Vehicle.default_driver_id != None)  # noqa: E711
                ),
            )
            .all()
        )
