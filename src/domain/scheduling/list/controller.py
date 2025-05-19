from datetime import datetime
from typing import Any, List, Tuple, Type

from dateutil.relativedelta import relativedelta
from PySide6.QtCore import QItemSelection
from sqlalchemy import Select

from common.controller.base_controller import BaseController
from common.controller.base_entity_controller import ModelType
from common.controller.base_list_controller import BaseListController
from domain.scheduling.add.controller import SchedulingAddController
from domain.scheduling.change.controller import SchedulingChangeController
from domain.scheduling.list.widget import (
    SchedulingDateTypeFilterEnum,
    SchedulingListWidget,
)
from domain.scheduling.model import Scheduling
from domain.scheduling.remove.controller import SchedulingRemoveController
from domain.scheduling.view.controller import SchedulingViewController


class SchedulingListController(BaseListController[Scheduling]):
    _widget: SchedulingListWidget

    def __init__(self, caller: BaseController | None = None):
        super().__init__(rows_per_page=25, caller=caller)

    def _get_widget_instance(self) -> SchedulingListWidget:
        return SchedulingListWidget()

    def _get_model_class(self) -> Type[ModelType]:
        return Scheduling

    def _apply_sorting(self, query: Select) -> Select:
        return query.order_by(Scheduling.datetime.asc())

    def _build_list_filters(self) -> List[Any]:
        filters = []
        type_filter = self._widget.type_filter.itemData(
            self._widget.type_filter.currentIndex()
        )
        year, month, day = self._widget.date_filter.date().getDate()
        start_date, end_date = self._build_start_end_date_filters(
            type_filter, year, month, day
        )
        filters.append(Scheduling.datetime.between(start_date, end_date))
        print(start_date.strftime("%Y-%m-%d %H:%M:%S"))
        print(end_date.strftime("%Y-%m-%d %H:%M:%S"))
        roadman_exists_filter = self._widget.roadmap_exists_filter.get_current_data()
        if roadman_exists_filter is not None:
            filters.append(
                Scheduling.roadmap_id.isnot(None)
                if roadman_exists_filter
                else Scheduling.roadmap_id.is_(None)
            )
        return filters

    def _build_start_end_date_filters(
        self, type_filter: str, year: int, month: int, day: int
    ) -> Tuple[datetime, datetime]:
        start_date = datetime(year, month, day)
        end_date = datetime(year, month, day) + relativedelta(days=1)
        if type_filter == SchedulingDateTypeFilterEnum.WEEK.name:
            start_date -= relativedelta(days=start_date.weekday() + 1)
            end_date = start_date + relativedelta(days=7)
        elif type_filter == SchedulingDateTypeFilterEnum.MONTH.name:
            start_date = datetime(year, month, 1)
            end_date = start_date + relativedelta(months=1)
        elif type_filter == SchedulingDateTypeFilterEnum.YEAR.name:
            start_date = datetime(year, 1, 1)
            end_date = start_date + relativedelta(years=1)
        return start_date, end_date

    def _set_widget_connections(self) -> None:
        super()._set_widget_connections()
        self._widget.add_button.clicked.connect(self.__add_button_clicked)
        self._widget.change_button.clicked.connect(self.__change_button_clicked)
        self._widget.remove_button.clicked.connect(self.__remove_button_clicked)
        self._widget.view_button.clicked.connect(self.__view_button_clicked)

    def __add_button_clicked(self) -> None:
        self.add_controller = SchedulingAddController(self)
        self.add_controller.show()

    def __change_button_clicked(self) -> None:
        self.change_controller = SchedulingChangeController(self._selected_model, self)
        self.change_controller.show()

    def __remove_button_clicked(self) -> None:
        self.remove_controller = SchedulingRemoveController(self._selected_model, self)
        self.remove_controller.show()

    def __view_button_clicked(self) -> None:
        self.view_controller = SchedulingViewController(self._selected_model, self)
        self.view_controller.show()

    def _on_table_selection_changed(
        self, selected: QItemSelection, deselected: QItemSelection
    ) -> None:
        super()._on_table_selection_changed(selected, deselected)
        if self._selected_model and self._selected_model.roadmap:
            self._widget.change_button.setDisabled(True)
            self._widget.remove_button.setDisabled(True)
