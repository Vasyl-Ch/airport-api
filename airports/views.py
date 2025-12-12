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


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.select_related("source", "destination")
    serializer_class = RouteSerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]

    def get_serializer_class(self):
        if self.action == "list":
            return RouteListSerializer
        elif self.action == "retrieve":
            return RouteDetailSerializer
        return RouteSerializer
