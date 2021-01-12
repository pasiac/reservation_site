from django.contrib import admin

from ticket.models import Reservation, Ticket, TicketReservation

admin.site.register(Ticket)
admin.site.register(TicketReservation)
admin.site.register(Reservation)
