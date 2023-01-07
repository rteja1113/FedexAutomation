import json
import os
from typing import List
import logging
import pymongo
from aggregateStats.models import AggregatedDriverInfo, AggregatedPreLoadInfo
from aggregateStats.utils import compute_hours
# logger = logging.getLogger()


# TODO: need to add logging to this module
def insert_weekly_schedule(file_path: str):
    """
    given a path to the json document containing a collection of daily services of drivers,
    will insert it into the mongodb.
    """

    daily_service = json.load(open(file_path, "r"))
    client = pymongo.MongoClient(os.environ.get("MONGO_URL"), 27017)
    db = client["FedexDB"]
    fedex_driver_collection = db["FedexDriverDailyService"]
    for dto in daily_service["item"]["v1"]["planDtos"]:
        # if dto["deliveryDate"] not in fedex_driver_collection:
        for individual_scanner in dto["scanners"]:
            if individual_scanner["onRoadHours"]:
                individual_scanner["onRoadHoursFloat"] = compute_hours(individual_scanner["onRoadHours"])
            else:
                individual_scanner["onRoadHoursFloat"] = 0.0
            if individual_scanner["onDutyHours"]:
                individual_scanner["onDutyHoursFloat"] = compute_hours(individual_scanner["onDutyHours"])
            else:
                individual_scanner["onDutyHoursFloat"] = 0.0

    fedex_driver_collection.insert_many(daily_service["item"]["v1"]["planDtos"])

    return


def aggregate_stops_and_packages_by_driver_and_route(start_date: int, end_date: int) -> List:
    """
    Aggregates actual stops and actual packages per driver based on the given start and end dates(inclusive on both)
    NOTE: it already accounts for route splitting

    start_date: <int> yyyymmdd
    end_date: <int> yyyymmdd
    ex: start_date = 20221101, end_date=20221130, returns the total actual stops and actual packages for every driver
    """
    client = pymongo.MongoClient(os.environ.get("MONGO_URL"), 27017)
    db = client["FedexDB"]
    fedex_driver_collection = db["FedexDriverDailyService"]

    pipeline = [
        {
            '$unwind': {
                'path': '$scanners'
            }
        }, {
            '$match': {
                'deliveryDate': {
                    '$gte': start_date,
                    '$lte': end_date
                }
            }
        }, {
            '$group': {
                '_id': {'driverName': '$scanners.driverName', 'route': '$workAreaNumber'},
                'totalPackages': {
                    '$sum': '$scanners.packages'
                },
                'totalStops': {
                    '$sum': '$scanners.stops'
                },
                'totalOnRoadHours': {
                    '$sum': '$scanners.onRoadHoursFloat'
                },
                'totalOnDutyHours': {
                    '$sum': '$scanners.onDutyHoursFloat'
                }
            }
        }
    ]
    agg_results = list(fedex_driver_collection.aggregate(pipeline))
    agg_results = [AggregatedDriverInfo(driver_name=agg_result["_id"]["driverName"],
                                         route_id=agg_result["_id"]["route"],
                                         actual_stops=agg_result["totalStops"],
                                         actual_packages=agg_result["totalPackages"],
                                         total_road_hours=agg_result["totalOnRoadHours"],
                                         total_onduty_hours=agg_result["totalOnDutyHours"])
                   for agg_result in agg_results]
    return agg_results


def aggregate_preload_stops_and_packages_by_route(start_date: int, end_date: int) -> List:
    """
    Aggregates preload stops and packages per route based on the given start and dates(inclusive on both)

    :param start_date: <int> yyyymmdd
    :param end_date: <int> yyyymmdd
    ex: start_date = 20221101, end_date=20221130, returns the total stops and packages for every route
    """

    client = pymongo.MongoClient(os.environ.get("MONGO_URL"), 27017)
    db = client["FedexDB"]
    fedex_driver_collection = db["FedexDriverDailyService"]

    pipeline = [
        {
            '$match': {
                'deliveryDate': {
                    '$gte': start_date,
                    '$lte': end_date
                }
            }
        }, {
            '$group': {
                '_id': {'route': '$workAreaNumber'},
                'totalPackages': {
                    '$sum': '$scannedPackages'
                },
                'totalStops': {
                    '$sum': '$scannedStops'
                }
            }
        }
    ]
    agg_results = list(fedex_driver_collection.aggregate(pipeline))
    return [AggregatedPreLoadInfo(agg_result["_id"]["route"], agg_result["totalStops"], agg_result["totalPackages"])
            for agg_result in agg_results]


if __name__ == "__main__":
    all_files = ["../datasets/11052022.json",
                 "../datasets/11122022.json",
                 "../datasets/11252022.json",
                 "../datasets/12022022.json",
                 "../datasets/12092022.json",
                 "../datasets/12162022.json",
                 "../datasets/12232022.json"]

    for json_doc in all_files:
        insert_weekly_schedule(json_doc)
    # aggregate_preload_stops_and_packages_by_route(20221101, 20221223)