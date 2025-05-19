from typing import Type

from PySide6.QtCore import QDate, QTime
from PySide6.QtWidgets import QTableWidgetItem

from common.controller.base_entity_controller import ModelType
from common.controller.base_view_controller import BaseViewController
from common.gui.widget.base_view_widget import BaseViewWidget
from domain.roadmap.model import Roadmap
from domain.roadmap.view.widget import RoadmapViewWidget


class RoadmapViewController(BaseViewController[Roadmap]):
    _widget: RoadmapViewWidget

    def _populate_view(self, entity: Roadmap) -> None:
        self._widget.date_field.setDate(
            QDate(
                entity.departure.year,
                entity.departure.month,
                entity.departure.day,
            )
        )
        self._widget.driver_field.setText(entity.driver.get_combo_box_description())
        self._widget.vehicle_field.setText(entity.vehicle.get_combo_box_description())
        for scheduling in entity.schedulings:
            row_count = self._widget.schedulings_table.rowCount()
            self._widget.schedulings_table.insertRow(row_count)
            self._widget.schedulings_table.setItem(
                row_count, 0, QTableWidgetItem(str(scheduling.id))
            )
            self._widget.schedulings_table.setItem(
                row_count, 1, QTableWidgetItem(scheduling.get_description())
            )
        self._widget.departure_time_field.setTime(
            QTime(
                entity.departure.hour,
                entity.departure.minute,
            )
        )
        self._widget.arrival_time_field.setTime(
            QTime(
                entity.arrival.hour,
                entity.arrival.minute,
            )
        )
        self._widget.creation_user_field.setText(
            entity.creation_user.get_combo_box_description()
        )

    def _get_widget_instance(self) -> BaseViewWidget:
        return RoadmapViewWidget()

    def _get_model_class(self) -> Type[ModelType]:
        return Roadmap
