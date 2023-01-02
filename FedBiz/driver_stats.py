from mongo_crud_utils import aggregate_stops_and_packages_by_driver

if __name__ == "__main__":
    results = aggregate_stops_and_packages_by_driver(start_date=20221101, end_date=20221223)
    print(results)
