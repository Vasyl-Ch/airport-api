from django.db import models
from django.core.exceptions import ValidationError

from flights.models import Flight
from users.models import User


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="orders"
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order #{self.id} by {self.user} at {self.created_at}"


class Ticket(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="tickets"
    )
    flight = models.ForeignKey(
        Flight,
        on_delete=models.CASCADE,
        related_name="tickets"
    )
    row = models.IntegerField()
    seat = models.IntegerField()

    class Meta:
        unique_together = ["flight", "row", "seat"]

    def __str__(self):
        return (f"Ticket #{self.id} "
                f"Flight #{self.flight.id} for "
                f"{self.flight} - Row {self.row}, "
                f"Seat {self.seat}")

    def clean(self):
        if self.row > self.flight.airplane.rows:
            raise ValidationError(
                f"Row number cannot exceed {self.flight.airplane.rows}"
            )
        if self.seat > self.flight.airplane.seats_in_row:
            raise ValidationError(
                f"Seat number cannot exceed "
                f"{self.flight.airplane.seats_in_row}"
            )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
