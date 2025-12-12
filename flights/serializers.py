from drf_spectacular.types import OpenApiTypes
from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field

from flights.models import (
    Flight,
    AirplaneType,
    Airplane,
    Crew
)


class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = ["id", "name"]


class AirplaneSerializer(serializers.ModelSerializer):
    capacity = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Airplane
        fields = [
            "id",
            "name",
            "airplane_type",
            "rows",
            "seats_in_row",
            "capacity"
        ]


class AirplaneListSerializer(AirplaneSerializer):
    airplane_type = serializers.CharField(read_only=True)
    capacity = serializers.SerializerMethodField()

    @extend_schema_field(int)
    def get_capacity(self, obj: Airplane) -> int:
        return obj.capacity


class AirplaneDetailSerializer(AirplaneSerializer):
    airplane_type = AirplaneTypeSerializer(read_only=True)
    capacity = serializers.SerializerMethodField()

    @extend_schema_field(int)
    def get_capacity(self, obj: Airplane) -> int:
        return obj.capacity


class CrewSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Crew
        fields = ["id", "first_name", "last_name", "full_name"]
    
    @extend_schema_field(str)
    def get_full_name(self, obj: Crew) -> str:
        return obj.full_name


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = [
            "id",
            "departure_time",
            "arrival_time",
            "airplane",
            "route",
            "crew"
        ]


class FlightListSerializer(FlightSerializer):
    airplane = serializers.CharField(source="airplane.name", read_only=True)
    route = serializers.StringRelatedField(read_only=True)
    airplane_capacity = serializers.IntegerField(source="airplane.capacity", read_only=True)
    tickets_available = serializers.SerializerMethodField()

    @extend_schema_field(int)
    def get_tickets_available(self, obj: Flight) -> int:
        return obj.airplane.capacity - getattr(obj, "tickets_count", 0)

    class Meta:
        model = Flight
        fields = [
            "id",
            "route",
            "airplane",
            "airplane_capacity",
            "departure_time",
            "arrival_time",
            "tickets_available"
        ]



class FlightDetailSerializer(FlightSerializer):
    airplane = AirplaneDetailSerializer(read_only=True)
    route = serializers.StringRelatedField(read_only=True)
    crew = CrewSerializer(many=True, read_only=True)
    taken_seats = serializers.SerializerMethodField()

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_taken_seats(self, obj: Flight) -> list[dict[str, int]]:
        return [
            {"row": ticket.row, "seat": ticket.seat}
            for ticket in obj.tickets.all()
        ]

    class Meta:
        model = Flight
        fields = [
            "id",
            "route",
            "airplane",
            "departure_time",
            "arrival_time",
            "crew",
            "taken_seats",
        ]
