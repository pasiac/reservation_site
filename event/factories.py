import datetime

import factory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyDateTime
from pytz import UTC

from event.models import Event


class EventFactory(DjangoModelFactory):
    name = factory.Sequence(lambda n: "name_%d" % n)
    date = FuzzyDateTime(datetime.datetime(2008, 1, 1, tzinfo=UTC))

    class Meta:
        model = Event
