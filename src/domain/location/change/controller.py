from typing import Any, Dict, Optional, Type

from common.controller.base_change_controller import BaseChangeController
from common.controller.base_entity_controller import ModelType
from common.gui.widget.base_change_widget import BaseChangeWidget
from common.model.column_types.point import Coordinate
from domain.location.change.widget import LocationChangeWidget
from domain.location.model import Location


class LocationChangeController(BaseChangeController[Location]):
    _widget: LocationChangeWidget

    def _populate_form(self, entity: Location) -> None:
        self._widget.description_field.setText(entity.description)
        self._widget.latitude = entity.coordinates.latitude
        self._widget.longitude = entity.coordinates.longitude
        self._widget.coordinates_field.setText(
            f"{entity.coordinates.latitude}, {entity.coordinates.longitude}"
        )

    def _get_model_updates(self) -> Optional[Dict[str, Any]]:
        description = self._widget.description_field.text()
        if not description:
            self._widget.show_info_pop_up("Atenção", "A descrição é obrigatória")
            return None
        if hasattr(self._widget, "latitude") and hasattr(self._widget, "longitude"):
            coordinates = Coordinate(
                latitude=self._widget.latitude,
                longitude=self._widget.longitude,
            )
        return {
            "description": description.strip(),
            "coordinates": coordinates,
        }

    def _get_widget_instance(self) -> BaseChangeWidget:
        return LocationChangeWidget()

    def _get_model_class(self) -> Type[ModelType]:
        return Location
