from django.urls import path
from .views import *

app_name = 'base'

urlpatterns = [
    path("", index, name="index"),
    path("search", search, name="search"),
    path('event/<int:event_id>', event_detail, name='event_detail'),
]