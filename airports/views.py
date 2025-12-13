from django.db.models import Prefetch
from rest_framework import viewsets

from airports.models import (
    Airport,
    Route
)
from airports.serializers import (
    AirportSerializer,
    AirportListSerializer,
    AirportDetailSerializer,
    RouteSerializer,
    RouteListSerializer,
    RouteDetailSerializer,
)
from config.permissions import IsAdminOrIfAuthenticatedReadOnly
from flights.models import Flight


class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]

    def get_serializer_class(self):
        if self.action == "list":
            return AirportListSerializer
        elif self.action == "retrieve":
            return AirportDetailSerializer
        return AirportSerializer

    def get_queryset(self):
        queryset = self.queryset

        if self.action == "retrieve":
            queryset = queryset.prefetch_related(
                Prefetch(
                    "source_routes",
                    queryset=Route.objects.select_related("destination")
                ),
                Prefetch(
                    "destination_routes",
                    queryset=Route.objects.select_related("source")
                )
            )

        return queryset


class RouteViewSet(viewsets.ModelViewSet):
    serializer_class = RouteSerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]

    def get_queryset(self):
        queryset = Route.objects.select_related("source", "destination")

        if self.action == "retrieve":
            queryset = queryset.prefetch_related(
                Prefetch(
                    "flights",
                    queryset=Flight.objects.select_related(
                        "airplane__airplane_type",
                        "route__source",
                        "route__destination"
                    )
                )
            )

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return RouteListSerializer
        elif self.action == "retrieve":
            return RouteDetailSerializer
        return RouteSerializer
