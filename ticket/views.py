from django.views.generic import DetailView, CreateView, ListView, FormView
from ticket.models import Ticket, Reservation
from ticket.forms import TicketReservationForm, PaymentForm
from django.urls import reverse_lazy
from decimal import Decimal
from utils.payment import PaymentGateway
from datetime import datetime
from django.shortcuts import redirect


class TicketDetailView(DetailView):
    model = Ticket


class TicketReservationCreateView(CreateView):
    template_name = "ticket/ticket_reservation_form.html"
    form_class = TicketReservationForm
    success_url = reverse_lazy("reservation_list")

    def form_valid(self, form):
        obj = form.save(commit=False)
        user = self.request.user
        reservation = Reservation.objects.filter(reserved_by=user, active=True, paid=False).first()
        if not reservation:
            reservation = Reservation.objects.create(reserved_by=user, paid=False, active=True)
        obj.reservation = reservation
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
        reservation = Reservation.objects.get(reserved_by=request.user, active=True, paid=False)
        cost = reservation.calculate_total_tickets_cost()
        if not reservation:
            return self.form_invalid(form)
        
        # I am not sure if I cant pass parameter message this way
        if reservation.is_expired():
            reservation.delete()
            return redirect('reservation_list', message="Reservation expired")

        if form.is_valid():
            payment.charge(cost, "paid")
            reservation.paid = True
            reservation.paid_time = datetime.now()
            reservation.save()
        else:
            return self.form_invalid(form)