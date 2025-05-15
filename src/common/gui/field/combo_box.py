from typing import Any, Generic, List, Type, TypeVar, Union

from PySide6.QtWidgets import QComboBox

from common.model.base_model import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)


class ComboBox(QComboBox, Generic[ModelType]):
    model_class: Type[ModelType]
    _data: List[ModelType]

    def __init__(
        self,
        parent=None,
        model_class: Type[ModelType] = None,
        default_none: bool = True,
        load: bool = True,
        **kwargs: Any,
    ):
        self.model_class = model_class
        super().__init__(parent)
        if load:
            self.fill(default_none, **kwargs)

    def fill(self, default_none: bool = True, **kwargs: Any) -> None:
        self.clear()
        if default_none:
            self.addItem("", None)
        for item in self._list_for_fill(**kwargs):
            self._data.append(item)
            self.addItem(item.get_combo_box_description(), item)

    def _list_for_fill(self, **kwargs: Any) -> List[ModelType]:
        return self.model_class.list_for_combo_box(**kwargs)

    def get_data(self) -> List[ModelType]:
        return self._data

    def setCurrentIndexByData(self, data_value: Any) -> None:
        index = next(i for i in range(self.count()) if self.itemData(i) == data_value)
        self.setCurrentIndex(index)

    def get_current_data(self) -> Union[ModelType, None]:
        return self.itemData(self.currentIndex())

    def clear(self) -> None:
        super().clear()
        self._data = []
