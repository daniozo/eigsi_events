import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from dashboard.forms import NewEventForm
from dashboard.models import Event, Participation, Operation
from dashboard.operation_types import OperationTypes
from django.utils import timezone
from datetime import timedelta



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
    extended_date = event.date + timedelta(days=31)

    if request.user.is_authenticated:
        participation = Participation.objects.filter(event_id=event_id, user=request.user).first()
        context = {
            'event': event,
            'user_is_ghost': request.user.groups.filter(name='Ghost').exists(),
            'participation': participation,
            'is_future_event': event.date > now,
            'is_excessed_date': extended_date < now
        }
        return render(request, 'base/event_detail.html', context)

    context = {
        'event': event,
        'participation': None,
        'is_future_event': event.date > now
    }
    return render(request, 'base/event_detail.html', context)


def create_event(request):
    if request.method == 'POST':
        form = NewEventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = NewEventForm()

    return render(request, 'base/create_event.html', {'form': form})


def event_registration(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if event.date < now:
        messages.error(request, "Cet évènement est passé.")
        return redirect('base:event_detail', event_id=event_id)

    def create_participation(is_pending, operation_type):
        Participation.objects.create(
            event=event,
            user=request.user,
            is_pending=is_pending,
            is_registered=not is_pending
        )
        Operation.objects.create(
            author=request.user,
            type=operation_type,
            content_object=event
        )

    def register_eigsi_member():
        if event.price:
            create_participation(is_pending=True, operation_type=OperationTypes.REQUESTED_REGISTRATION.value)
            messages.info(request, "Votre inscription est en cours de validation.")
            print("Votre inscription est en cours de validation.")
        else:
            create_participation(is_pending=False, operation_type=OperationTypes.REGISTERED.value)
            messages.success(request, "Inscription réussie.")
            print("Inscription réussie.")

    if request.method == 'POST':

        existing_registration = Participation.objects.filter(event=event, user=request.user).exists()

        if existing_registration:
            messages.info(request, "Vous êtes déjà inscrit à cet évènement !")
            print("Vous êtes déjà inscrit à cet évènement !")
            return redirect('dashboard:event_detail', event_id=event_id)

        if event.is_public:
            if request.user.groups.filter(name='Ghost').exists():
                create_participation(is_pending=True, operation_type=OperationTypes.REQUESTED_REGISTRATION.value)
                messages.info(request, "Votre inscription est en cours de validation.")
                print("Votre inscription est en cours de validation.")
            else:
                register_eigsi_member()
        else:
            if request.user.groups.filter(name='Ghost').exists():
                messages.error(request, "L'inscription à cet évènement est uniquement réservée aux membres de l'EIGSI.")
                print("L'inscription à cet évènement est uniquement réservée aux membres de l'EIGSI.")
            else:
                register_eigsi_member()

    return redirect('base:event_detail', event_id=event_id)

@login_required
def rate_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    extended_date = event.date + timedelta(days=31)

    response = "Cet évènement est dépassé et ne peut plus être noté."

    if extended_date < now:
        return JsonResponse({"response": response})

    if request.method == 'POST':
        data = json.loads(request.body)
        rating = data.get("rate")
        if rating not in [int(i) for i in range(1, 6)]:
            response = "Veuillez fournir une note valide."
            return JsonResponse({"response": response})

        try:
            participation = Participation.objects.get(event=event, user=request.user)
            participation.rating = int(rating)
            participation.save()
            response = "Votre note a été mise à jour avec succès."
        except Participation.DoesNotExist:
            Participation.objects.create(
                event=event,
                user=request.user,
                rating=int(rating),
                is_pending=False,
                is_registered=True,
            )
            response = "Vous avez été inscrit et votre note a été enregistrée avec succès."

    return JsonResponse({"response": response})