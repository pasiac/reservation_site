from django.db import models
from event.models import Event
from django.contrib.auth.models import User
from decimal import Decimal
import datetime


class Ticket(models.Model):
    name = models.CharField(max_length=32)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Reservation(models.Model):
    reserved_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    paid = models.BooleanField(default=False)
    paid_time = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=True)
    experation_time = models.DateTimeField(default=datetime.datetime.now() + datetime.timedelta(minutes=15), blank=True)

    def calculate_total_tickets_cost(self):
        reserved_tickets = self.ticketreservation_set.all()
        total_cost = sum(Decimal(str(reserved_ticket.quantity)) * reserved_ticket.ticket.price for reserved_ticket in reserved_tickets)
        return total_cost

    def is_expired(self):
        now = datetime.datetime.now()
    
        if self.experation_time.replace(tzinfo=None) < now:
            return True
        return False

class TicketReservation(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    reservation = models.ForeignKey(
        Reservation, null=True, blank=True, on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.ticket} {self.quantity}"
