from django.urls import path
from event.views import EventListView, EventDetailView

urlpatterns = [
    path("", EventListView.as_view(), name="event_list"),
    path("<int:pk>/", EventDetailView.as_view(), name="event_detail"),
]
