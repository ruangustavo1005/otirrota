from typing import List

from common.gui.field.combo_box import ComboBox
from domain.driver.model import Driver


class ActiveDriversComboBox(ComboBox[Driver]):
    def __init__(self, default_none: bool = True, parent=None):
        super().__init__(parent, model_class=Driver, default_none=default_none)

    def _list_for_fill(self) -> List[Driver]:
        return Driver.query().filter(Driver.active == True).all()  # noqa: E712
