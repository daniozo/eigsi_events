from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from dashboard.forms import NewEventForm
from dashboard.models import Event

now = timezone.now()


def index(request):
    events = Event.objects.filter(date__gte=now, archived_at=None).order_by('date')[:4]
    return render(request, 'base/index.html', {'events': events})


def search(request):
    start = 2016
    year = now.year
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
    events = Event.objects.filter(status=True, archived_at=None).order_by('date')

    has_events = len(events) != 0

    context = {'has_events': has_events, 'events': events, 'start': start, 'years': years,
               'event_type': event_type}

    return render(request, 'base/search.html', context)


def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'base/event_detail.html', {'event': event})


def create_event(request):
    if request.method == 'POST':
        form = NewEventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = NewEventForm()

    return render(request, 'base/create_event.html', {'form': form})
