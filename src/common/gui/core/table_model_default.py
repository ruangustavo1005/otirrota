from typing import Any, List, Union, Generic, TypeVar, Type

from PySide6.QtCore import QAbstractTableModel, QModelIndex, QPersistentModelIndex, Qt

from common.model.base_model import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)


class TableModelDefault(QAbstractTableModel, Generic[ModelType]):
    def __init__(self, model_class: Type[ModelType], data: List[List[Any]] = None):
        super(TableModelDefault, self).__init__()
        self._model_class = model_class
        self._headers = model_class.get_table_columns()
        self._data = data or []
        self._original_objects: List[ModelType] = []

    def rowCount(self, parent: Union[QModelIndex, QPersistentModelIndex] = None):
        return len(self._data)

    def columnCount(self, parent: Union[QModelIndex, QPersistentModelIndex] = None):
        return len(self._headers)

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if (
            role == Qt.ItemDataRole.DisplayRole
            and orientation == Qt.Orientation.Horizontal
            and section < len(self._headers)
        ):
            return self._headers[section]
        return None

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            return self._data[index.row()][index.column()]
        return None

    def get_original_object(self, row: int) -> ModelType:
        if 0 <= row < len(self._original_objects):
            return self._original_objects[row]
        return None

    def setRowData(self, row: int, values: List[Any]) -> bool:
        if row < 0 or row >= self.rowCount() or len(values) != self.columnCount():
            return False
        for col in range(self.columnCount()):
            self._data[row][col] = values[col]
            index = self.createIndex(row, col)
            self.dataChanged.emit(index, index, [Qt.ItemDataRole.EditRole])
        return True

    def set_data_from_objects(self, objects: List[ModelType]) -> bool:
        if not objects:
            self.beginResetModel()
            self._data = []
            self._original_objects = []
            self.endResetModel()
            return True

        self._original_objects = objects
        formatted_data = [obj.format_for_table() for obj in objects]
        return self.setData(formatted_data)

    def setData(self, data: List[List[Any]]) -> bool:
        if len(data) == 0 or (len(data) > 0 and len(data[0]) == len(self._headers)):
            self.beginResetModel()
            self._data = data
            self.endResetModel()
            return True
        return False
