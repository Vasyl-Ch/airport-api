from rest_framework import serializers

from airports.models import (
    Airport,
    Route
)


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ["id", "name", "closest_big_city"]


class AirportListSerializer(AirportSerializer):
    pass


class AirportDetailSerializer(AirportSerializer):
    source_routes = serializers.StringRelatedField(
        many=True,
        read_only=True
    )
    destination_routes = serializers.StringRelatedField(
        many=True,
        read_only=True
    )

    class Meta:
        model = Airport
        fields = [
            "id",
            "name",
            "closest_big_city",
            "source_routes",
            "destination_routes"
        ]


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ["id", "source", "destination", "distance"]



class RouteListSerializer(RouteSerializer):
    source = serializers.CharField(source="source.name", read_only=True)
    destination = serializers.CharField(source="destination.name", read_only=True)


class RouteDetailSerializer(RouteSerializer):
    source = AirportSerializer(read_only=True)
    destination = AirportSerializer(read_only=True)
    flights = serializers.StringRelatedField(read_only=True, many=True)

    class Meta:
        model = Route
        fields = [
            "id",
            "source",
            "destination",
            "distance",
            "flights"
        ]

