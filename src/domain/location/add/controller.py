from typing import Optional, Type

from common.controller.base_add_controller import BaseAddController
from common.controller.base_entity_controller import ModelType
from common.gui.widget.base_add_widget import BaseAddWidget
from common.model.column_types.point import Coordinate
from domain.config.model import Config
from domain.location.add.widget import LocationAddWidget
from domain.location.model import Location


class LocationAddController(BaseAddController[Location]):
    _widget: LocationAddWidget

    def _get_populated_model(self) -> Optional[Location]:
        description = self._widget.description_field.text()
        if not description:
            self._widget.show_info_pop_up("Atenção", "A descrição é obrigatória")
            return None

        if self._widget.coordinates_field.text():
            coordinates = Coordinate(
                latitude=self._widget.latitude,
                longitude=self._widget.longitude,
            )
        else:
            self._widget.show_info_pop_up("Atenção", "As coordenadas são obrigatórias")
            return None

        return Location(
            description=description.strip(),
            coordinates=coordinates,
        )

    def _get_widget_instance(self) -> BaseAddWidget:
        config = Config.get_config()
        if config.departure_coordinates:
            return LocationAddWidget(
                latitude=config.departure_coordinates.latitude,
                longitude=config.departure_coordinates.longitude,
            )
        return LocationAddWidget()

    def _get_model_class(self) -> Type[ModelType]:
        return Location
