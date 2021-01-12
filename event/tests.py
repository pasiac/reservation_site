from django.test import TestCase

from accounts.factories import UserFactory
from event.factories import EventFactory
from utils.tests.mixins import TestUtilityMixin


class TestEventListView(TestCase, TestUtilityMixin):
    def setUp(self):
        self.user = UserFactory.create()
        self.event = EventFactory.create()

    def test_user_see_list_of_events(self):
        url = "/event/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, self.STATUS_OK)
        self.assertContains(response, self.event.name)

    def test_user_see_event_details(self):
        url = f"/event/{self.event.pk}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, self.STATUS_OK)
        self.assertContains(response, self.event.name)
