from typing import Any, Dict, Optional, Type

from common.controller.base_change_controller import BaseChangeController
from common.controller.base_entity_controller import ModelType
from common.gui.widget.base_change_widget import BaseChangeWidget
from common.model.column_types.point import Coordinate
from domain.config.change.widget import ConfigChangeWidget
from domain.config.model import Config


class ConfigChangeController(BaseChangeController[Config]):
    _widget: ConfigChangeWidget

    def _populate_form(self, entity: Config) -> None:
        self._widget.department_name_field.setText(entity.department_name)
        self._widget.body_name_field.setText(entity.body_name)
        self._widget.eplison_field.setValue(entity.eplison)
        self._widget.minpts_field.setValue(entity.minpts)
        self._widget.distance_matrix_api_key_field.setText(
            entity.distance_matrix_api_key
        )
        if entity.departure_coordinates:
            self._widget.departure_coordinates_field.setText(
                f"{entity.departure_coordinates.latitude}, {entity.departure_coordinates.longitude}"
            )
            self._widget.latitude = entity.departure_coordinates.latitude
            self._widget.longitude = entity.departure_coordinates.longitude

    def _get_model_updates(self) -> Optional[Dict[str, Any]]:
        department_name = self._widget.department_name_field.text()
        if not department_name:
            self._widget.show_info_pop_up(
                "Atenção", "O nome da secretaria é obrigatório"
            )
            return None

        body_name = self._widget.body_name_field.text()
        if not body_name:
            self._widget.show_info_pop_up("Atenção", "O nome do órgão é obrigatório")
            return None

        eplison = self._widget.eplison_field.value()
        if not eplison:
            self._widget.show_info_pop_up("Atenção", "O epsilon é obrigatório")
            return None

        minpts = self._widget.minpts_field.value()
        if not minpts:
            self._widget.show_info_pop_up("Atenção", "O minpts é obrigatório")
            return None

        distance_matrix_api_key = self._widget.distance_matrix_api_key_field.text()
        if not distance_matrix_api_key:
            self._widget.show_info_pop_up(
                "Atenção", "A chave da distance matrix api é obrigatório"
            )
            return None

        if self._widget.departure_coordinates_field.text():
            coordinates = Coordinate(
                latitude=self._widget.latitude,
                longitude=self._widget.longitude,
            )
        else:
            self._widget.show_info_pop_up(
                "Atenção", "As coordenadas do ponto de partida são obrigatórias"
            )
            return None

        return {
            "department_name": department_name.strip(),
            "body_name": body_name.strip(),
            "eplison": eplison,
            "minpts": minpts,
            "distance_matrix_api_key": distance_matrix_api_key.strip(),
            "departure_coordinates": coordinates,
        }

    def _get_widget_instance(self) -> BaseChangeWidget:
        return ConfigChangeWidget()

    def _get_model_class(self) -> Type[ModelType]:
        return Config
