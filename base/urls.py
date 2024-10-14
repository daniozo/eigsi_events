from django.urls import path
from .views import *

app_name = 'base'

urlpatterns = [
    path("", index, name="index"),
    path("events", events, name="events"),
    path("search", search, name="search"),
    path('event/<int:event_id>', event_detail, name='event_detail'),
    path("create", create_event, name='create_event'),
]