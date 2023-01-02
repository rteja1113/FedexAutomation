import json
import logging
import pymongo

# logger = logging.getLogger()


# TODO: need to add logging to this module
def insert_weekly_schedule(file_path: str):
    """
    given a path to the json document containing a collection of daily services of drivers,
    will insert it into the mongodb.
    """
    daily_service = json.load(open(file_path, "r"))
    client = pymongo.MongoClient('localhost', 27017)
    db = client["FedexDB"]
    fedex_driver_collection = db["FedexDriverDailyService"]
    fedex_driver_collection.insert_many(daily_service["item"]["v1"]["planDtos"])
    return


def aggregate_stops_and_packages_by_driver(start_date: int, end_date: int):
    """
    Aggregates actual stops and actual packages per driver based on the given dates
    NOTE: it already accounts for route splitting

    start_date: <int> yyyymmdd
    end_date: <int> yyyymmdd
    ex: start_date = 20221101, end_date=20221130, returns the total actual stops and actual packages for every driver
    """
    client = pymongo.MongoClient('localhost', 27017)
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
                '_id': '$scanners.driverName',
                'totalPackages': {
                    '$sum': '$scanners.packages'
                },
                'totalStops': {
                    '$sum': '$scanners.stops'
                }
            }
        }
    ]
    agg_results = fedex_driver_collection.aggregate(pipeline)
    return list(agg_results)


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