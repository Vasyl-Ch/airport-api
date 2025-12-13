from django.contrib import admin
from airports.models import Airport, Route


@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    list_display = ["name", "closest_big_city"]
    search_fields = ["name", "closest_big_city"]


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ["source", "destination", "distance"]
    list_filter = ["source", "destination"]
    search_fields = ["source__name", "destination__name"]
