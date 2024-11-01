from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone

from dashboard.forms import NewEventForm, EventGalleryForm
from dashboard.models import Event, EventGallery

from django.views.decorators.csrf import csrf_exempt
from base.chatbot.rag_handler import RAGHandler
import json

rag_handler = RAGHandler()


@csrf_exempt
def chat(request):
    if rag_handler.vector_store is None:
        events = Event.objects.all()
        rag_handler.create_vector_store(events)

    if request.method == "POST":
        data = json.loads(request.body)
        query = data.get("query")
        chat_history = data.get("chat_history", [])

        response = rag_handler.get_response(query, chat_history)
        return JsonResponse({"response": response})


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


def auth(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(name__in=['Admin', 'SuperAdmin']).exists():
            return redirect(request.GET.get('next', 'dashboard/index'))
        return redirect(request.GET.get('next', '/'))

    if request.method == 'GET' and 'error' in request.GET:
        messages.error(request, "Erreur lors de la connexion. Veuillez réessayer.")

    return render(request, 'auth.html')


@login_required
def index(request):
    upcoming_events = Event.objects.filter(date__gte=now, archived_at=None, status=True).count()
    pending_events = Event.objects.filter(status=False, archived_at=None).count()
    all_events = Event.objects.count()
    # TODO: get recent activities

    context = {'upcoming_events': upcoming_events, 'pending_events': pending_events,
               'all_events': all_events}

    return render(request, 'dashboard/index.html', context)


@login_required
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

    search = request.GET.get('search', '')
    event_type_filter = request.GET.get('event_type', '')
    accessibility = request.GET.get('accessibility', '')
    year_filter = request.GET.get('year', '')

    event_s = Event.objects.all()

    if search:
        event_s = event_s.filter(title__icontains=search) | event_s.filter(description__icontains=search)

    if event_type_filter:
        event_s = event_s.filter(event_type=event_type_filter)

    if accessibility:
        is_public = accessibility == 'public'
        event_s = event_s.filter(is_public=is_public)

    if year_filter:
        event_s = event_s.filter(date__year=year_filter)

    has_events = len(event_s) != 0
    years = list(range(year, start - 1, -1))

    context = {
        'has_events': has_events,
        'events': event_s,
        'start': start,
        'years': years,
        'event_type': event_type,
        'now': now,
        'search': search,
        'event_type_filter': event_type_filter,
        'accessibility': accessibility,
        'year_filter': year_filter
    }

    return render(request, 'dashboard/events.html', context)


@login_required
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
        'is_super_admin': request.user.groups.filter(name="SuperAdmin").exists()
    }

    return render(request, 'dashboard/event_settings/event_settings.html', context)


@login_required
def approve_event(request, event_id):
    if request.method == 'POST':
        event = get_object_or_404(Event, id=event_id)
        event.status = True
        event.save()
        messages.success(request, "L'événement a été approuvé avec succès.")
        return redirect('dashboard:event_settings', event_id=event_id)


@login_required
def archive_event(request, event_id):
    if request.method == 'POST':
        event = get_object_or_404(Event, id=event_id)
        event.archived_at = now
        event.save()
        messages.success(request, "L'événement a été bien archivé.")
        return redirect('dashboard:event_settings', event_id=event_id)


@login_required
def unarchive_event(request, event_id):
    if request.method == 'POST':
        event = get_object_or_404(Event, id=event_id)
        event.archived_at = None
        event.save()
        messages.success(request, "L'événement a été bien désarchivé.")
        return redirect('dashboard:event_settings', event_id=event_id)


@login_required
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


@login_required
def delete_gallery_image(request, image_id):
    image = get_object_or_404(EventGallery, id=image_id)
    if request.method == 'POST':
        image.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)


@login_required
def stats(request):
    events_stats = {
        "inscriptions": Event.objects.filter(status="inscription").count(),
        "participations": Event.objects.filter(type="participation").count(),
    }

    return JsonResponse(events_stats)


@login_required
def users(request):
    context = {
        'users': User.objects.filter(groups__name__in=['Student']).order_by('username'),
    }
    return render(request, 'dashboard/users.html', context)


@login_required
def dashboard(request):
    return render(request, 'dashboard/dashboard.html')