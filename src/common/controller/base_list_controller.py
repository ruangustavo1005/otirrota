import math
from abc import abstractmethod
from typing import Any, Generic, List, Optional

from PySide6.QtCore import QItemSelection, QModelIndex
from sqlalchemy import Select, func, select

from common.controller.base_controller import BaseController, ModelType
from common.gui.widget.base_list_widget import BaseListWidget
from db import Database


class BaseListController(BaseController[ModelType], Generic[ModelType]):
    _widget: BaseListWidget[ModelType]
    _selected_data: List[Any] | None = None
    _selected_model: Optional[ModelType] = None
    _selected_row: int = -1

    def __init__(
        self,
        rows_per_page: int = 20,
        caller: BaseController | None = None,
    ) -> None:
        self._rows_per_page = rows_per_page
        self._model_class = self._get_model_class()
        super().__init__(caller)
        self._set_widget_connections()

    @abstractmethod
    def _get_widget_instance(self) -> BaseListWidget[ModelType]:
        raise NotImplementedError()

    def _set_widget_connections(self) -> None:
        self._widget.update_button.clicked.connect(self._update_button_clicked)
        self._widget.page_field.returnPressed.connect(self._page_field_return_pressed)
        self._widget.first_page_button.clicked.connect(self._first_page_button_clicked)
        self._widget.before_page_button.clicked.connect(
            self._before_page_button_clicked
        )
        self._widget.after_page_button.clicked.connect(self._after_page_button_clicked)
        self._widget.last_page_button.clicked.connect(self._last_page_button_clicked)

        self._widget.add_button.clicked.connect(self._add_button_clicked)
        self._widget.change_button.clicked.connect(self._change_button_clicked)
        self._widget.remove_button.clicked.connect(self._remove_button_clicked)
        self._widget.view_button.clicked.connect(self._view_button_clicked)

        self._widget.table.selectionModel().selectionChanged.connect(
            self._on_table_selection_changed
        )
        self._widget.table.doubleClicked.connect(self._on_table_double_clicked)

    def _update_button_clicked(self) -> None:
        self._widget.page_field.setText("1")
        self.update_table_data()

    def _on_table_selection_changed(
        self, selected: QItemSelection, deselected: QItemSelection
    ):
        indexes = selected.indexes()
        if indexes:
            self._selected_row = indexes[0].row()
            self._selected_data = [index.data() for index in indexes]
            self._selected_model = self._widget.table_model.get_original_object(
                self._selected_row
            )
            self._widget.enable_row_actions()
        else:
            self._selected_row = -1
            self._selected_data = None
            self._selected_model = None
            self._widget.disable_row_actions()

    def _on_table_double_clicked(self, index: QModelIndex) -> None:
        if index.isValid():
            self._selected_row = index.row()
            self._selected_model = self._widget.table_model.get_original_object(
                self._selected_row
            )
            if self._selected_model:
                self._change_button_clicked()

    def _page_field_return_pressed(self) -> None:
        page = int(self._widget.page_field.text())
        if page > self._page_count:
            self._widget.page_field.setText(str(self._page_count))
        elif page < 1:
            self._widget.page_field.setText("1")
        self.update_table_data()

    def _first_page_button_clicked(self) -> None:
        self._widget.page_field.setText("1")
        self.update_table_data()

    def _before_page_button_clicked(self) -> None:
        page = int(self._widget.page_field.text())
        self._widget.page_field.setText(str(max(page - 1, 1)))
        self.update_table_data()

    def _after_page_button_clicked(self) -> None:
        page = int(self._widget.page_field.text())
        self._widget.page_field.setText(str(min(page + 1, self._page_count)))
        self.update_table_data()

    def _last_page_button_clicked(self) -> None:
        self._widget.page_field.setText(str(self._page_count))
        self.update_table_data()

    def _add_button_clicked(self) -> None:
        pass

    def _change_button_clicked(self) -> None:
        pass

    def _remove_button_clicked(self) -> None:
        pass

    def _view_button_clicked(self) -> None:
        pass

    def show(self) -> None:
        self.update_table_data()
        super().show()

    def update_table_data(self) -> None:
        self._widget.disable_row_actions()
        self._selected_data = None
        self._selected_model = None
        self._selected_row = -1

        self.close_session_if_exists()

        self._update_row_count()
        self._update_page_count()

        results = self._list()
        self._widget.table_model.set_data_from_objects(results)

    def _list(self) -> List[ModelType]:
        page = int(self._widget.page_field.text())
        limit = self._rows_per_page
        offset = (page - 1) * limit

        filters = self._build_list_filters()

        self._session = Database.get_session()
        try:
            query = select(self._model_class).filter(*filters)

            query = self._apply_sorting(query)

            query = query.limit(limit).offset(offset)

            results = list(self._session.execute(query).scalars().all())

            self._session.commit()

            return results
        except Exception as e:
            self._session.rollback()
            raise e

    def _apply_sorting(self, query: Select) -> Select:
        return query.order_by(self._model_class.id.desc())

    def _build_list_filters(self) -> List:
        return []

    def _update_row_count(self) -> None:
        with Database.session_scope() as session:
            filters = self._build_list_filters()
            query = select(func.count()).select_from(self._model_class).filter(*filters)
            self._row_count = session.execute(query).scalar() or 0
            self._widget.set_row_count(self._row_count, self._rows_per_page)

    def _update_page_count(self) -> None:
        self._page_count = max(math.ceil(self._row_count / self._rows_per_page), 1)
        self._widget.set_page_count(self._page_count)

    def close(self) -> None:
        self.close_session_if_exists()
        super().close()

    def close_session_if_exists(self):
        if hasattr(self, "_session") and self._session:
            self._session.close()
            self._session = None
