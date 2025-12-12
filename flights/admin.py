from django.contrib import admin
from flights.models import AirplaneType, Airplane, Crew, Flight


@admin.register(AirplaneType)
class AirplaneTypeAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]


@admin.register(Airplane)
class AirplaneAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "airplane_type",
        "rows",
        "seats_in_row",
        "capacity"
    ]
    list_filter = ["airplane_type"]
    search_fields = ["name"]


@admin.register(Crew)
class CrewAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name"]
    search_fields = ["first_name", "last_name"]


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ["route", "airplane", "departure_time", "arrival_time"]
    list_filter = ["departure_time", "airplane"]
    search_fields = ["route__source__name", "route__destination__name"]
    filter_horizontal = ["crew"]
