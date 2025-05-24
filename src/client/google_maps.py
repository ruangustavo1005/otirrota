from googlemaps import Client

from common.model.column_types.point import Coordinate


class GoogleMapsClient:
    def __init__(self, client: Client) -> None:
        self.__client = client

    def get_travel_time_between(
        self, origin: Coordinate, destination: Coordinate
    ) -> int:
        response = self.__client.distance_matrix(
            origins=[f"{origin.latitude},{origin.longitude}"],
            destinations=[f"{destination.latitude},{destination.longitude}"],
            mode="driving",
            language="pt-BR",
        )
        return response["rows"][0]["elements"][0]["duration"]["value"]
