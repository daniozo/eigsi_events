from django.urls import path
from .views import *

app_name = 'dashboard'

urlpatterns = [
    path("", index, name="index"),
    path("events/", events, name="events"),
    path("event/<int:event_id>", event_settings, name="event_settings"),
    path('events/<int:event_id>/approve/', approve_event, name='approve_event'),
    path('events/<int:event_id>/archive/', archive_event, name='archive_event'),
    path('events/<int:event_id>/unarchive/', unarchive_event, name='unarchive_event'),
    path('events/<int:event_id>/delete/', delete_event, name='delete_event'),
    path('events/<int:event_id>/gallery/add/', add_gallery_images, name='add_gallery_images'),
    path('gallery/image/<int:image_id>/delete/', delete_gallery_image, name='delete_gallery_image'),
    path("users/", users, name="users"),
]
