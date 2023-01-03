from constants import MINUTES_PER_HOUR


def compute_hours(hour_mins: str) -> int:
    hours, mins = hour_mins.split(":")
    return int(hours) + (int(mins) / MINUTES_PER_HOUR)