from datetime import datetime

from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, FormView, ListView

from ticket.forms import PaymentForm, TicketReservationForm
from ticket.models import Reservation, Ticket, TicketReservation
from utils.payment import PaymentGateway

# TODO:
# 1. Decrease quantity of tickets when reserved
# 2. If reservation expired increase quantity of tickets available
# 3. Create view with statistics
# 4. Rewrite paymentview
# 5. Create possibility to pass message to reservation_list
# 6. Check clean code issues reservation have path "orders" and so one
# 5. Write tests


class TicketDetailView(DetailView):
    model = Ticket


class TicketReservationCreateView(CreateView):
    template_name = "ticket/ticket_reservation_form.html"
    form_class = TicketReservationForm
    model = TicketReservation
    success_url = reverse_lazy("reservation_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"event_id": self.kwargs.get("event_id")})
        return kwargs

    def form_valid(self, form):
        obj = form.save(commit=False)
        user = self.request.user
        reservation = Reservation.objects.filter(
            reserved_by=user, active=True, paid=False
        ).first()
        if not reservation:
            reservation = Reservation.objects.create(
                reserved_by=user, paid=False, active=True
            )
        obj.reservation = reservation
        obj.ticket.quantity -= obj.quantity
        obj.save()
        return super().form_valid(form)


class ReservationListView(ListView):
    model = Reservation

    def get_queryset(self):
        return Reservation.objects.filter(reserved_by=self.request.user)


class ReservationDetailView(DetailView):
    model = Reservation

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tickets_cost = self.object.calculate_total_tickets_cost()
        context["total_amount"] = tickets_cost
        return context


class PaymentView(FormView):
    form_class = PaymentForm
    template_name = "ticket/ticket_reservation_form.html"
    success_url = reverse_lazy("reservation_list")

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        payment = PaymentGateway()
        reservation = Reservation.objects.get(
            reserved_by=request.user, active=True, paid=False
        )
        cost = reservation.calculate_total_tickets_cost()
        if not reservation:
            return self.form_invalid(form)

        # There should be options to pass messsage message="Reservation expired"
        if reservation.is_expired():
            self._resolve_available_tickets(reservation)
            reservation.delete()
            return redirect("reservation_list")

        # There should be validation with payment class to make use of exceptions
        # And also a  message="Your payment was successful!"
        # TODO: Change reservation list to accept message
        if form.is_valid():
            payment.charge(cost, "paid")
            reservation.paid = True
            reservation.paid_time = datetime.now()
            reservation.save()
            return redirect("reservation_list")
        else:
            return self.form_invalid(form)

    def _resolve_available_tickets(self, reservation):
        """
        Increase number of available tickets from reservation that expired
        @param reservation: expired reservation
        """
        ticket_reservations = reservation.tickereservation_set.all()
        for ticket_reservation in ticket_reservations:
            ticket_reservation.ticket.quantity += ticket_reservation.quantity
            ticket_reservation.save()
