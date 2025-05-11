from typing import Type

from common.controller.base_entity_controller import ModelType
from common.controller.base_view_controller import BaseViewController
from common.gui.widget.base_view_widget import BaseViewWidget
from domain.scheduling.model import Scheduling
from PySide6.QtCore import QDateTime, QDate, QTime

from domain.scheduling.view.widget import SchedulingViewWidget


class SchedulingViewController(BaseViewController[Scheduling]):
    _widget: SchedulingViewWidget

    def _populate_view(self, entity: Scheduling) -> None:
        self._widget.datetime_field.setDateTime(
            QDateTime(
                QDate(entity.datetime.year, entity.datetime.month, entity.datetime.day),
                QTime(entity.datetime.hour, entity.datetime.minute, entity.datetime.second),
            )
        )
        self._widget.average_duration_field.setTime(
            QTime(
                entity.average_duration.hour,
                entity.average_duration.minute,
                entity.average_duration.second,
            )
        )
        self._widget.patient_field.setText(entity.patient.get_combo_box_description() if entity.patient else "")
        self._widget.location_field.setText(entity.location.get_combo_box_description())
        self._widget.purpose_field.setText(entity.purpose.get_combo_box_description())
        self._widget.sensitive_patient_checkbox.setChecked(bool(entity.sensitive_patient))
        self._widget.description_field.setText(entity.description)
        self._widget.companions_widget.set_companions(entity.companions)

    def _get_widget_instance(self) -> BaseViewWidget:
        return SchedulingViewWidget()

    def _get_model_class(self) -> Type[ModelType]:
        return Scheduling
