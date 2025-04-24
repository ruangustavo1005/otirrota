from typing import Any

from PySide6.QtWidgets import QComboBox


class ComboBox(QComboBox):
    def setCurrentIndexByData(self, data_value: Any) -> None:
        index = next(i for i in range(self.count()) if self.itemData(i) == data_value)
        self.setCurrentIndex(index)
