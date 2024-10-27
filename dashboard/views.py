from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from dashboard.forms import NewEventForm
from dashboard.models import Event
import datetime


now = timezone.now()

def index(request):
    upcoming_events = Event.objects.filter(date__gte=now).count()
    pending_events = Event.objects.filter(status=False).count()
    all_events = Event.objects.count()
    # TODO: get recent activities

    context = {'upcoming_events': upcoming_events, 'pending_events': pending_events,
               'all_events': all_events, 'nbs': range(9)}

    return render(request, 'dashboard/index.html', context)


def events(request):
    if request.method == 'POST':
        form = NewEventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('events')
    else:
        form = NewEventForm()

    start = 2016
    year = now.year

    event_s = Event.objects.all()

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

    years = list(range(year, start - 1, -1))

    context = {'events': event_s, 'start': start, 'years': years, 'event_type': event_type}

    return render(request, 'dashboard/events.html', context)


def event_settings(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    has_stats = False

    if event.date < now:
        has_stats = True

    context = {'event': event, 'has_stats': has_stats}

    return render(request, 'dashboard/event_settings.html', context)


def stats(request):
    events_stats = {
        "inscriptions": Event.objects.filter(status="inscription").count(),
        "participations": Event.objects.filter(type="participation").count(),
    }

    return JsonResponse(events_stats)


def dashboard(request):
    return render(request, 'dashboard/dashboard.html')
