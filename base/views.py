from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .models import Event
from .forms import EventForm
import datetime

now = datetime.datetime.now()

def index(request):
    events = Event.objects.filter(date__gte=timezone.now()).order_by('date')[:4]
    return render(request, 'index.html', {'events': events})

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
    events = Event.objects.all()

    return render(request, 'search.html', {'events': events, 'nbr': range(len(events)), 'start': start, 'years': years, 'event_type': event_type})

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'event_detail.html', {'event': event})

def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventForm()

    return render(request, 'create_event.html', {'form': form})
