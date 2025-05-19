from typing import Union

from PySide6.QtWidgets import QComboBox


class BooleanComboBox(QComboBox):
    def __init__(
        self,
        parent=None,
    ):
        super().__init__(parent)
        self.fill()

    def fill(self) -> None:
        self.clear()
        self.addItem("", None)
        self.addItem("Sim", True)
        self.addItem("Não", False)

    def setCurrentIndexByData(self, data_value: Union[bool, None]) -> None:
        if data_value is None:
            self.setCurrentIndex(0)
        else:
            index = next(
                i for i in range(self.count()) if self.itemData(i) == data_value
            )
            self.setCurrentIndex(index)

    def get_current_data(self) -> Union[bool, None]:
        return self.itemData(self.currentIndex())
