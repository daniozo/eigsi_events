from django.shortcuts import render, redirect, get_object_or_404
from .models import Event
from .forms import EventForm
import datetime

def index(request):
  return render(request, 'index.html')


def events(request):
    now = datetime.datetime.now()
    start = 2016
    year = now.year
    event_type = ['Conférence', 'Atelier', 'Journée culturel', 'Ftour', 'Compétition', 'Caritatif', 'Eigsi Got Talent', 'Journée d\'intégration', 'Autres']

    years = list(range(year, start - 1, -1))
    events = Event.objects.all()

    return render(request, 'events.html', {'events': events, 'nbr': range(len(events)), 'start': start, 'years': years, 'event_type': event_type})

def search(request):
    now = datetime.datetime.now()
    start = 2016
    year = now.year
    event_type = ['Conférence', 'Atelier', 'Journée culturel', 'Ftour', 'Compétition', 'Caritatif', 'Eigsi Got Talent', 'Journée d\'intégration', 'Autres']

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
