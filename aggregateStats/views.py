from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework import serializers
from .mongo_crud_utils import aggregate_stops_and_packages_by_driver_and_route,\
    aggregate_preload_stops_and_packages_by_route, insert_weekly_schedule
# Create your views here.

@api_view(['GET'])
def home(request):
    api_urls = {
        "Uploading Driver Schedule": "/upload-driver-schedule/",
        "Actual Stops and Packages b/w start and end date per route per driver": "actual-aggregation/?startDate=<int>&endDate=<int>/",
        "Preload Stops and Packages b/w stat and end date per route": "preload-aggregation/?startDate=<int>&endDate<int"
    }
    return Response(api_urls)
#
#

@api_view(['POST'])
def add_daily_service(request: Request):
    insert_weekly_schedule(request.data)
    return Response("Successfully Uploaded", status=status.HTTP_201_CREATED)

@api_view(['GET'])
def actual_agg(request):
    return HttpResponse("Please enter start date and end date in the url")

@api_view(['GET'])
def actual_agg_view(request: Request) -> HttpResponse:
    """
    aggregates actual stops and packages for every driver based on start and end date
    :param request:
    :param start_date: start date in yyyymmdd format
    :param end_date: end date in yyyymmdd format
    :return:
    """
    context = {
        "start_date": int(request.query_params.get("startDate")),
        "end_date": int(request.query_params.get("endDate")),
    }
    agg_result = aggregate_stops_and_packages_by_driver_and_route(context["start_date"], context["end_date"])
    return Response(agg_result, status=status.HTTP_200_OK)


def preload_agg(request):
    return HttpResponse("Please enter start date and end date in the url")


@api_view(['GET'])
def preload_agg_view(request) -> HttpResponse:
    """
    aggregates preload stops and packages for every route based on start and end date
    :param request:
    :param start_date: start date in yyyymmdd format
    :param end_date: end date in yyyymmdd format
    :return:
    """
    context = {
        "start_date": int(request.query_params.get("startDate")),
        "end_date": int(request.query_params.get("endDate")),
    }
    agg_result = aggregate_preload_stops_and_packages_by_route(context["start_date"], context["end_date"])
    return Response(agg_result, status=status.HTTP_200_OK)
