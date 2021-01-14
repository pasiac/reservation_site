import factory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyDateTime, FuzzyInteger
from pytz import UTC

from ticket.models import Ticket
from event.factories import EventFactory


class TicketFactory(DjangoModelFactory):
    name = factory.Sequence(lambda n: "name_%d" % n)
    price = 10.20
    quantity = FuzzyInteger(0, 42)
    event = factory.SubFactory(EventFactory)

    class Meta:
        model = Ticket
