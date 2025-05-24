from googlemaps import Client

from client.google_maps import GoogleMapsClient
from domain.config.model import Config


class GoogleMapsClientFactory:
    @staticmethod
    def create() -> GoogleMapsClient:
        config = Config.get_config()
        return GoogleMapsClient(client=Client(config.distance_matrix_api_key))
