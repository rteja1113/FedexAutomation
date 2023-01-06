from django.shortcuts import render
from django.http import HttpResponse
from .mongo_crud_utils import aggregate_stops_and_packages_by_driver_and_route,\
    aggregate_preload_stops_and_packages_by_route
# Create your views here.


def home(request):
    context = {
        "myname": "Ravi Teja",
        "mymeas": [10, 11]
    }
    return render(request, 'index.html', context)
#
#


def actual_agg(request):
    return HttpResponse("Please enter start date and end date in the url")


def actual_agg_view(request, start_date: int, end_date: int) -> HttpResponse:
    """
    aggregates actual stops and packages for every driver based on start and end date
    :param request:
    :param start_date: start date in yyyymmdd format
    :param end_date: end date in yyyymmdd format
    :return:
    """
    context = {
        "start_date": start_date,
        "end_date": end_date,
    }
    agg_result = aggregate_stops_and_packages_by_driver_and_route(start_date, end_date)
    context["aggregated_stats"] = agg_result
    return render(request, "basic_table.html", context)


def preload_agg(request):
    return HttpResponse("Please enter start date and end date in the url")


def preload_agg_view(request, start_date: int, end_date: int) -> HttpResponse:
    """
    aggregates preload stops and packages for every route based on start and end date
    :param request:
    :param start_date: start date in yyyymmdd format
    :param end_date: end date in yyyymmdd format
    :return:
    """
    context = {
        "start_date": start_date,
        "end_date": end_date,
    }
    agg_result = aggregate_preload_stops_and_packages_by_route(start_date, end_date)
    context["aggregated_stats"] = agg_result
    return render(request, "basic_table_2.html", context)

