from django.test import RequestFactory, TestCase
from .views import TicketDetailView


class TestTicketDetailView(TestCase):
    def test_context_contain_ticket_object(self):
        request = RequestFactory().get("/")
        view = HomeView()
        view.setup(request)

        context = view.get_context_data()
        self.assertIn("environment", context)
