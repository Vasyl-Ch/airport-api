from django.db.models import Prefetch
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from orders.models import Order, Ticket
from orders.serializers import (
    OrderSerializer,
    OrderListSerializer,
    OrderDetailSerializer
)


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related(
            Prefetch(
                "tickets",
                queryset=Ticket.objects.select_related(
                    "flight__route__source",
                    "flight__route__destination",
                    "flight__airplane__airplane_type"
                ).prefetch_related("flight__crew")
            )
        )

    def get_serializer_class(self):
        if self.action == "list":
            return OrderListSerializer
        if self.action == "retrieve":
            return OrderDetailSerializer
        return OrderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
