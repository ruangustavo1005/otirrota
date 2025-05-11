from typing import Generic, List, Optional, Type, TypeVar

from PySide6.QtCore import QEvent, QStringListModel, Qt, QTimer, Signal
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QFrame,
    QLineEdit,
    QListView,
)

from common.model.base_model import BaseModel
from db import Database

ModelType = TypeVar("ModelType", bound=BaseModel)


class ResultsPopup(QListView):
    item_selected = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(
            Qt.Tool | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint
        )
        self.setFrameStyle(QFrame.Box | QFrame.Plain)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setAttribute(Qt.WA_DeleteOnClose, False)
        self.setAttribute(Qt.WA_ShowWithoutActivating, True)

    def hideEvent(self, event):
        super().hideEvent(event)
        QApplication.removeEventFilter(self.parent())

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() in (Qt.Key_Up, Qt.Key_Down, Qt.Key_PageUp, Qt.Key_PageDown):
            super().keyPressEvent(event)
            return

        if event.key() == Qt.Key_Return:
            index = self.currentIndex()
            if index.isValid():
                self.item_selected.emit(index.row())
            self.hide()
            return

        if event.key() == Qt.Key_Escape:
            self.hide()
            return

        self.parent().keyPressEvent(event)

    def mouseReleaseEvent(self, event):
        index = self.indexAt(event.pos())
        if index.isValid():
            self.item_selected.emit(index.row())
            self.hide()


class SearchLineEdit(QLineEdit, Generic[ModelType]):
    model_changed = Signal(object)

    def __init__(
        self,
        parent=None,
        model_class: Type[ModelType] = None,
        min_chars_for_search: int = 1,
        max_results: int = 10,
    ):
        try:
            model_class.apply_text_search_filter(None, "")
        except NotImplementedError:
            raise ValueError(
                f"O modelo {model_class.__name__} não implementa o método apply_text_search_filter"
            )
        except Exception:
            pass
        super().__init__(parent)
        self.model_class = model_class
        self.selected_model: Optional[ModelType] = None
        self.min_chars_for_search = min_chars_for_search
        self.max_results = max_results
        self._filtered_items = []
        self._item_descriptions = []
        self._popup_visible = False
        self._db_session = None

        self.setPlaceholderText(f"Pesquisar {self.model_class.get_static_description()}...")

        self.popup = ResultsPopup(self)
        self.popup.item_selected.connect(self._on_item_selected)
        self.popup.hide()

        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)
        self.search_timer.setInterval(300)
        self.search_timer.timeout.connect(self._perform_search)

        self.textChanged.connect(self._on_text_changed)

        self.installEventFilter(self)

    def _on_text_changed(self, text: str) -> None:
        if (
            self.selected_model
            and text != self.selected_model.get_combo_box_description()
        ):
            self.set_selected_model(None)

        text = text.strip()
        if len(text) >= self.min_chars_for_search:
            self.search_timer.start()
        else:
            self.popup.hide()
            self._popup_visible = False
            self._filtered_items = []
            self._item_descriptions = []

    def _perform_search(self) -> None:
        if self.selected_model is not None:
            return

        search_text = self.text().strip()
        if len(search_text) < self.min_chars_for_search:
            return

        if self._db_session:
            try:
                self._db_session.close()
            except:  # noqa: E722
                pass
            self._db_session = None

        self._db_session = Database.get_session()

        try:
            query = self._db_session.query(self.model_class)
            query = self.model_class.apply_text_search_filter(query, search_text).limit(
                self.max_results
            )
            filtered_items: Optional[List[ModelType]] = query.all()

            self._filtered_items = filtered_items
            self._item_descriptions = []

            if not filtered_items:
                self.popup.hide()
                self._popup_visible = False
                return

            for item in filtered_items:
                desc = item.get_combo_box_description()
                self._item_descriptions.append(desc)

            model = QStringListModel(self._item_descriptions)
            self.popup.setModel(model)

            self._show_popup()
        except Exception:
            if self._db_session:
                self._db_session.close()
                self._db_session = None

    def _show_popup(self) -> None:
        width = self.width()
        row_count = self.popup.model().rowCount()
        row_height = self.popup.sizeHintForRow(0)
        height = min(200, row_height * min(7, row_count) + 4)

        position = self.mapToGlobal(self.rect().bottomLeft())

        self.popup.setGeometry(position.x(), position.y(), width, height)

        if row_count > 0:
            self.popup.setCurrentIndex(self.popup.model().index(0, 0))

        self.popup.show()
        self._popup_visible = True
        QApplication.instance().installEventFilter(self)

    def _on_item_selected(self, index: int) -> None:
        if 0 <= index < len(self._filtered_items):
            self.set_selected_model(self._filtered_items[index])
            if 0 <= index < len(self._item_descriptions):
                self.setText(self._item_descriptions[index])
            else:
                self.setText(self.selected_model.get_combo_box_description())

            self.popup.hide()
            self._popup_visible = False

    def get_selected_model(self) -> Optional[ModelType]:
        return self.selected_model

    def set_selected_model(self, model: Optional[ModelType]) -> None:
        if model is None:
            self.selected_model = None
            self.setText("")
            self.model_changed.emit(None)
            return

        self.selected_model = model
        self.setText(model.get_combo_box_description())
        self.model_changed.emit(model)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if self._popup_visible:
            if event.key() in (
                Qt.Key_Up,
                Qt.Key_Down,
                Qt.Key_PageUp,
                Qt.Key_PageDown,
                Qt.Key_Return,
                Qt.Key_Escape,
            ):
                self.popup.keyPressEvent(event)
                return

        super().keyPressEvent(event)

    def focusOutEvent(self, event):
        QTimer.singleShot(100, self._check_focus_and_hide_popup)
        super().focusOutEvent(event)

    def _check_focus_and_hide_popup(self):
        if not self.hasFocus() and not self.popup.hasFocus():
            self.popup.hide()
            self._popup_visible = False

            if self._db_session:
                try:
                    self._db_session.close()
                except:  # noqa: E722
                    pass
                self._db_session = None

    def eventFilter(self, obj: object, event: QEvent) -> bool:
        if obj == self and event.type() == QEvent.MouseButtonPress:
            self.selectAll()

            text = self.text().strip()
            if len(text) >= self.min_chars_for_search and not self._popup_visible:
                self._perform_search()

            return False

        if self._popup_visible and event.type() == QEvent.MouseButtonPress:
            pos = event.globalPos()
            if not self.geometry().contains(
                self.mapFromGlobal(pos)
            ) and not self.popup.geometry().contains(pos):
                self.popup.hide()
                self._popup_visible = False
                QApplication.removeEventFilter(self)
                return True

        return super().eventFilter(obj, event)

    def __del__(self):
        if self._db_session:
            try:
                self._db_session.close()
            except:  # noqa: E722
                pass
