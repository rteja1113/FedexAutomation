from aggregateStats.constants import MINUTES_PER_HOUR


def compute_hours(hhmm: str) -> float:
    """
    returns float format in hours
    :param hhmm:
    :return:
    """

    hours, minutes = hhmm.split(":")
    return int(hours) + (int(minutes) / MINUTES_PER_HOUR)
