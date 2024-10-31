from django.http import JsonResponse
from django.contrib.auth.models import User, Group
from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm

from dashboard.forms import NewEventForm, EventGalleryForm
from dashboard.models import Event, EventGallery


now = timezone.now()

event_type = [
        ('conference', 'Conférence'),
        ('workshop', 'Atelier'),
        ('cultural', 'Culturel'),
        ('ftour', 'Ftour'),
        ('competition', 'Compétition'),
        ('charity', 'Caritatif'),
        ('talent_show', 'Eigsi Got Talent'),
        ('integration_day', 'Journée d\'intégration'),
        ('other', 'Autres'),
    ]

def index(request):
    upcoming_events = Event.objects.filter(date__gte=now, archived_at=None, status=True).count()
    pending_events = Event.objects.filter(status=False, archived_at=None).count()
    all_events = Event.objects.count()
    # TODO: get recent activities

    context = {'upcoming_events': upcoming_events, 'pending_events': pending_events,
               'all_events': all_events}

    return render(request, 'dashboard/index.html', context)


def events(request):
    if request.method == 'POST':
        form = NewEventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard:events')
    else:
        form = NewEventForm()

    start = 2016
    year = now.year

    event_s = (Event.objects
               # .filter(archived_at=None)
               .all())
    has_events = len(event_s) != 0

    years = list(range(year, start - 1, -1))

    context = {'has_events': has_events, 'events': event_s, 'start': start, 'years': years, 'event_type': event_type,
               'now': now}

    return render(request, 'dashboard/events.html', context)


def event_settings(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    has_stats = event.date < now

    if request.method == 'POST':
        form = NewEventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return redirect('dashboard:event_settings', event_id=event.id)
    else:
        form = NewEventForm(instance=event)

    context = {
        'event': event,
        'has_stats': has_stats,
        'form': form,
    }

    return render(request, 'dashboard/event_settings/event_settings.html', context)


def approve_event(request, event_id):
    if request.method == 'POST':
        event = get_object_or_404(Event, id=event_id)
        event.status = True
        event.save()
        messages.success(request, "L'événement a été approuvé avec succès.")
        return redirect('dashboard:event_settings', event_id=event_id)


def archive_event(request, event_id):
    if request.method == 'POST':
        event = get_object_or_404(Event, id=event_id)
        event.archived_at = now
        event.save()
        messages.success(request, "L'événement a été bien archivé.")
        return redirect('dashboard:event_settings', event_id=event_id)


def unarchive_event(request, event_id):
    if request.method == 'POST':
        event = get_object_or_404(Event, id=event_id)
        event.archived_at = None
        event.save()
        messages.success(request, "L'événement a été bien désarchivé.")
        return redirect('dashboard:event_settings', event_id=event_id)


def add_gallery_images(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        form = EventGalleryForm(request.POST, request.FILES)
        if form.is_valid():
            images = request.FILES.getlist('images')
            gallery_images = []

            for image in images:
                gallery_image = EventGallery.objects.create(
                    event=event,
                    image=image
                )
                gallery_images.append({
                    'id': gallery_image.id,
                    'url': gallery_image.image.url
                })

            return JsonResponse({
                'status': 'success',
                'images': gallery_images
            })
        else:
            return JsonResponse({
                'status': 'error',
                'errors': form.errors
            }, status=400)

    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'}, status=405)


def delete_gallery_image(request, image_id):
    image = get_object_or_404(EventGallery, id=image_id)
    if request.method == 'POST':
        image.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)


def stats(request):
    events_stats = {
        "inscriptions": Event.objects.filter(status="inscription").count(),
        "participations": Event.objects.filter(type="participation").count(),
    }

    return JsonResponse(events_stats)


def dashboard(request):
    return render(request, 'dashboard/dashboard.html')