from typing import Optional
from domain.driver.model import Driver
from domain.vehicle.model import Vehicle


class DriversVehiclesRelation:
    def __init__(
        self,
        driver: Optional[Driver] = None,
        vehicle: Optional[Vehicle] = None,
        on_call_driver: bool = False,
    ):
        self.driver = driver
        self.vehicle = vehicle
        self.on_call_driver = on_call_driver
