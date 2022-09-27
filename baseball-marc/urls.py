from django.urls import path
from . import views

app_name = "baseball"
urlpatterns = [
    path("", views.index, name="index"),
    path("standings", views.standings, name="standings"),
    path("advance-day", views.advance_date, name="advance-date"),
]
