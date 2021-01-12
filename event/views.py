from django.views.generic import DetailView, ListView

from event.models import Event
from ticket.models import Ticket


class EventListView(ListView):
    model = Event
    paginate_by = 10


class EventDetailView(DetailView):
    model = Event

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tickets"] = Ticket.objects.filter(event=context.get("object").pk).all()
        return context
