from django.db import models
from dataclasses import dataclass
# Create your models here.


class AggregatedDriverInfo:
    def __init__(self, driver_name: str, route_id: int, actual_stops: int,
                 actual_packages: int, total_road_hours: float, total_onduty_hours: float):
        self.driver_name = driver_name
        self.route_id = route_id
        self.actual_stops = actual_stops
        self.actual_packages = actual_packages
        self.total_road_hours = round(total_road_hours, 2)
        self.total_onduty_hours = round(total_onduty_hours, 2)
        if total_onduty_hours > 0:
            self.packages_per_duty_hour = round(actual_packages/total_onduty_hours, 2)
        else:
            self.packages_per_duty_hour = "Undefined"

@dataclass
class AggregatedPreLoadInfo:
    route_id: int
    total_stops: int
    total_packages: int
