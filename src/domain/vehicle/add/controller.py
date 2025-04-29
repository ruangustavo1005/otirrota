from typing import Optional, Type

from common.controller.base_add_controller import BaseAddController
from common.controller.base_entity_controller import ModelType
from common.gui.widget.base_add_widget import BaseAddWidget
from domain.vehicle.add.widget import VehicleAddWidget
from domain.vehicle.model import Vehicle


class VehicleAddController(BaseAddController[Vehicle]):
    _widget: VehicleAddWidget

    def _get_populated_model(self) -> Optional[Vehicle]:
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

        return Vehicle(
            license_plate=license_plate.strip(),
            description=description.strip(),
            capacity=int(capacity.strip()),
            default_driver_id=default_driver.id if default_driver else None,
        )

    def _get_widget_instance(self) -> BaseAddWidget:
        return VehicleAddWidget()

    def _get_model_class(self) -> Type[ModelType]:
        return Vehicle
