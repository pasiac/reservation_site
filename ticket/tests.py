from django.test import TestCase

from accounts.factories import UserFactory
from event.factories import EventFactory
from utils.tests.mixins import TestUtilityMixin
from ticket.factories import TicketFactory


class TestEventListView(TestCase, TestUtilityMixin):
    def setUp(self):
        self.user = UserFactory.create()
        self.event = EventFactory.create()
        self.ticket = TicketFactory.create(event=self.event)

    def test_user_see_ticket_details(self):
        url = f"/tickets/{self.ticket.pk}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, self.STATUS_OK)
        self.assertContains(response, self.ticket.name)
        self.assertContains(response, self.ticket.price)

    def test_user_see_reservation_form(self):
        url = f"/tickets/buy/{self.event.pk}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, self.STATUS_OK)
        self.assertContains(response, "Quantity")
        self.assertContains(response, "Ticket")
