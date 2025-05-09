from typing import Any, Dict, Optional, Type

from common.controller.base_change_controller import BaseChangeController
from common.controller.base_entity_controller import ModelType
from common.gui.widget.base_change_widget import BaseChangeWidget
from domain.vehicle.change.widget import VehicleChangeWidget
from domain.vehicle.model import Vehicle


class VehicleChangeController(BaseChangeController[Vehicle]):
    _widget: VehicleChangeWidget

    def _populate_form(self, entity: Vehicle) -> None:
        self._widget.license_plate_field.setText(entity.format_license_plate())
        self._widget.description_field.setText(entity.description)
        self._widget.capacity_field.setText(str(entity.capacity))
        self._widget.default_driver_combo_box.setCurrentIndexByData(
            entity.default_driver
        )
        self._widget.active_field.setChecked(entity.active)

    def _get_model_updates(self) -> Optional[Dict[str, Any]]:
        license_plate = (
            self._widget.license_plate_field.get_license_plate_alphanumeric()
        )
        if (
            not license_plate
            or not self._widget.license_plate_field.is_valid_license_plate()
        ):
            self._widget.show_info_pop_up("Atenção", "A placa informada não é válida")
            return None

        description = self._widget.description_field.text()
        if not description:
            self._widget.show_info_pop_up("Atenção", "A descrição é obrigatória")
            return None

        capacity = self._widget.capacity_field.text()
        if not capacity:
            self._widget.show_info_pop_up("Atenção", "A capacidade é obrigatória")
            return None

        default_driver = self._widget.default_driver_combo_box.get_current_data()

        return {
            "license_plate": license_plate.strip(),
            "description": description.strip(),
            "capacity": int(capacity.strip()),
            "default_driver_id": default_driver.id if default_driver else None,
            "active": self._widget.active_field.isChecked(),
        }

    def _get_widget_instance(self) -> BaseChangeWidget:
        return VehicleChangeWidget()

    def _get_model_class(self) -> Type[ModelType]:
        return Vehicle
