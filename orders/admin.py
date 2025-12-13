from django.contrib import admin
from orders.models import Order, Ticket


class TicketInline(admin.TabularInline):
    model = Ticket
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["user__email"]
    inlines = [TicketInline]


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ["id", "order", "flight", "row", "seat"]
    list_filter = ["flight"]
    search_fields = ["order__id", "flight__id"]
