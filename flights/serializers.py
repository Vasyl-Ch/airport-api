from rest_framework import serializers

from .models import Flight, AirplaneType, Airplane, Crew


class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = ["id", "name"]


class AirplaneSerializer(serializers.ModelSerializer):
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
    airplane_type = serializers.CharField(source="airplane_type.name", read_only=True)


class AirplaneDetailSerializer(AirplaneSerializer):
    airplane_type = AirplaneTypeSerializer(source="airplane_type", read_only=True)


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = ["id", "first_name", "last_name", "full_name"]


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
    route = serializers.StringRelatedField(source="route", read_only=True)
    airplane_capacity = serializers.IntegerField(source="airplane.capacity", read_only=True)
    tickets_available = serializers.SerializerMethodField()

    def get_tickets_available(self, obj):
        return obj.airplane.capacity - obj.tickets.count()

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
    airplane = AirplaneDetailSerializer(source="airplane", read_only=True)
    route = serializers.StringRelatedField(source="route", read_only=True)
    crew = CrewSerializer(source="crew", read_only=True)
    taken_seats = serializers.SerializerMethodField()

    def get_taken_seats(self, obj):
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
