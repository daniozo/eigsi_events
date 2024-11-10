from django.urls import path
from .chatbot.chat_view import chat
from .views import *


app_name = 'base'

urlpatterns = [
    path("", index, name="index"),
    path("search", search, name="search"),
    path('event/<int:event_id>', event_detail, name='event_detail'),
    path('event_registration/<int:event_id>', event_registration, name='event_registration'),
    path('chat/', chat, name='chat'),
]