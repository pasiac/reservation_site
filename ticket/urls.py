from django.urls import path

from ticket.views import (PaymentView, ReservationDetailView,
                          ReservationListView, TicketDetailView,
                          TicketReservationCreateView)

urlpatterns = [
    path("<int:pk>/", TicketDetailView.as_view(), name="ticket_details"),
    path(
        "buy/", TicketReservationCreateView.as_view(), name="ticket_reservation_create"
    ),
    path("orders/", ReservationListView.as_view(), name="reservation_list"),
    path(
        "orders/<int:pk>/", ReservationDetailView.as_view(), name="reservation_details"
    ),
    path("payment/", PaymentView.as_view(), name="payment_view"),
]
