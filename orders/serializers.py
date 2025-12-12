from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from orders.models import (
    Order,
    Ticket
)
from flights.serializers import FlightListSerializer


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = [
            "id",
            "flight",
            "row",
            "seat"
        ]

    def validate(self, attrs):
        data = super().validate(attrs)
        flight = attrs["flight"]
        row = attrs["row"]
        seat = attrs["seat"]
        if Ticket.objects.filter(flight=flight, row=row, seat=seat).exists():
            raise ValidationError("Ticket already exists")
        return data

class TicketListSerializer(TicketSerializer):
    flight = FlightListSerializer(read_only=True)

    class Meta:
        model = Ticket
        fields = [
            "id",
            "flight",
            "row",
            "seat"
        ]


class TicketSeatsSerializer(serializers.Serializer):
    class Meta:
        model = Ticket
        fields = [
            "row",
            "seat"
        ]


class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "created_at",
            "tickets"
        ]

    @transaction.atomic
    def create(self, validated_data):
        tickets_data = validated_data.pop("tickets")
        order = Order.objects.create(**validated_data)
        for ticket_data in tickets_data:
            Ticket.objects.create(order=order, **ticket_data)
        return order

class OrderListSerializer(OrderSerializer):
    tickets = TicketSerializer(many=True, read_only=True)


class OrderDetailSerializer(OrderSerializer):
    tickets = TicketListSerializer(many=True, read_only=True)
