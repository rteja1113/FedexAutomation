from django.urls import path
from .views import home, actual_agg, actual_agg_view, preload_agg, preload_agg_view

urlpatterns = [
    path('', home, name="fedexAutomation-home"),
    path('actual-aggregation/', actual_agg, name="act-agg"),
    path('actual-aggregation/<int:start_date>/<int:end_date>/', actual_agg_view, name="act-agg-start-end"),
    path('preload-aggregation/', preload_agg, name="preload-agg"),
    path('preload-aggregation/<int:start_date>/<int:end_date>/', preload_agg_view, name="preload-agg-start-end"),
]