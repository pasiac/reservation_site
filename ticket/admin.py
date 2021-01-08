from ticket.models import TicketReservation, Ticket, Reservation
from django.contrib import admin


admin.site.register(Ticket)
admin.site.register(TicketReservation)
admin.site.register(Reservation)
