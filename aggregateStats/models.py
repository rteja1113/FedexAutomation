from django.db import models
from dataclasses import dataclass
# Create your models here.


@dataclass
class AggregatedDriverStats:
    driver_name: str
    route_id: int
    actual_stops: int
    actual_packages: int

