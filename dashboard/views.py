from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from dashboard.forms import NewEventForm, EventGalleryForm
from dashboard.models import Event, EventGallery, Operation, Participation
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib import messages
from django.utils import timezone
from dashboard.operation_types import OperationTypes

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

def is_admin(user):
    return user.groups.filter(name='Admin').exists()

def is_super_admin(user):
    return user.groups.filter(name='SuperAdmin').exists()

def is_authorized(user):
    print(f"{user.username} {is_admin(user)} and {is_super_admin(user)}")
    return is_admin(user) or is_super_admin(user)

def auth(request):
    if request.user.is_authenticated:
        if is_authorized(request.user):
            return redirect(request.GET.get('next', 'dashboard/index'))
        return redirect(request.GET.get('next', '/'))

    if request.method == 'GET' and 'error' in request.GET:
        messages.error(request, "Erreur lors de la connexion. Veuillez réessayer.")

    return render(request, 'auth.html')


def access_denied(request):
    return render(request, 'access_denied.html')


@login_required
@user_passes_test(is_authorized, login_url='access_denied', redirect_field_name=None)
def index(request):
    upcoming_events = Event.objects.filter(date__gte=now, archived_at=None, status=True).count()
    pending_events = Event.objects.filter(status=False, archived_at=None).count()
    all_events = Event.objects.count()
    recent_activities = Operation.objects.all().order_by('-date_time')

    operation_type_titles = [
        ('added_event', "Évènement ajouté"),
        ('updated_event', "Évènement modifié"),
        ('approved_event', "Évènement approuvé"),
        ('archived_event', "Évènement archivé"),
        ('unarchived_event', "Évènement désarchivé"),
        ('deleted_event', "Évènement supprimé"),
        ('updated_gallery', "Galerie modifié"),
        ('add_user', "Utilisateur ajouté"),
        ('activate_user', "Utilisateur activé"),
        ('deactivate_user', "Utilisateur désactivé"),
        ('delete_user', "Utilisateur supprimé"),
    ]

    context = {'upcoming_events': upcoming_events, 'pending_events': pending_events,
               'all_events': all_events, 'recent_activities': recent_activities,
               'operation_type_titles': operation_type_titles, 'now': now}

    return render(request, 'dashboard/index.html', context)


@login_required
@user_passes_test(is_authorized, login_url='access_denied', redirect_field_name=None)
def events(request):
    if request.method == 'POST':
        form = NewEventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save()
            Operation.objects.create(
                author=request.user,
                type=OperationTypes.ADDED_EVENT.value,
                content_object=event
            )
            return redirect('dashboard:events')
    else:
        form = NewEventForm()

    start = 2016
    year = now.year

    search = request.GET.get('search', '')
    event_type_filter = request.GET.get('event_type', '')
    accessibility = request.GET.get('accessibility', '')
    year_filter = request.GET.get('year', '')
    page = request.GET.get('page', 1)

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

    paginator = Paginator(event_s, 15)
    try:
        events_page = paginator.page(page)
    except PageNotAnInteger:
        events_page = paginator.page(1)
    except EmptyPage:
        events_page = paginator.page(paginator.num_pages)

    has_events = len(event_s) != 0
    years = list(range(year, start - 1, -1))

    context = {
        'has_events': has_events,
        'events': events_page,
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
@user_passes_test(is_authorized, login_url='access_denied', redirect_field_name=None)
def event_settings(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    has_stats = event.date < now

    if request.method == 'POST':
        form = NewEventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            Operation.objects.create(
                author=request.user,
                type=OperationTypes.UPDATED_EVENT.value,
                content_object=event
            )
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
@user_passes_test(is_super_admin, login_url='access_denied', redirect_field_name=None)
def approve_event(request, event_id):
    if request.method == 'POST':
        event = get_object_or_404(Event, id=event_id)
        event.status = True
        event.save()
        Operation.objects.create(
            author=request.user,
            type=OperationTypes.APPROVED_EVENT.value,
            content_object=event
        )
        messages.success(request, "L'événement a été approuvé avec succès.")
        return redirect('dashboard:event_settings', event_id=event_id)


@login_required
@user_passes_test(is_super_admin, login_url='access_denied', redirect_field_name=None)
def archive_event(request, event_id):
    if request.method == 'POST':
        event = get_object_or_404(Event, id=event_id)
        event.archived_at = now
        event.save()
        Operation.objects.create(
            author=request.user,
            type=OperationTypes.ARCHIVED_EVENT.value,
            content_object=event
        )
        messages.success(request, "L'événement a été bien archivé.")
        return redirect('dashboard:event_settings', event_id=event_id)


@login_required
@user_passes_test(is_super_admin, login_url='access_denied', redirect_field_name=None)
def unarchive_event(request, event_id):
    if request.method == 'POST':
        event = get_object_or_404(Event, id=event_id)
        event.archived_at = None
        event.save()
        Operation.objects.create(
            author=request.user,
            type=OperationTypes.UNARCHIVED_EVENT.value,
            content_object=event
        )
        messages.success(request, "L'événement a été bien désarchivé.")
        return redirect('dashboard:event_settings', event_id=event_id)


@login_required
@user_passes_test(is_super_admin, login_url='access_denied', redirect_field_name=None)
def delete_event(request, event_id):
    if request.method == 'POST':
        event = get_object_or_404(Event, id=event_id)
        event_title = event.title

        if not request.user.groups.filter(name="SuperAdmin").exists():
            messages.error(request, "Vous n'avez pas les droits pour supprimer un événement.")
            return redirect('dashboard:event_settings', event_id=event_id)

        try:
            event.delete()
            Operation.objects.create(
                author=request.user,
                type=OperationTypes.DELETED_EVENT.value,
                content_title=event_title
            )
            messages.success(request, "L'événement a été supprimé avec succès.")
            return redirect('dashboard:events')

        except Exception as e:
            messages.error(request, "Une erreur est survenue lors de la suppression de l'événement.")
            return redirect('dashboard:event_settings', event_id=event_id)

    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'}, status=405)


@login_required
@user_passes_test(is_authorized, login_url='access_denied', redirect_field_name=None)
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

    return JsonResponse({'status': 'error', 'message': 'Requête invalide'}, status=405)


@login_required
@user_passes_test(is_authorized, login_url='access_denied', redirect_field_name=None)
def delete_gallery_image(request, image_id):
    image = get_object_or_404(EventGallery, id=image_id)
    if request.method == 'POST':
        image.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Requête invalide'}, status=400)


@login_required
@user_passes_test(is_authorized, login_url='access_denied', redirect_field_name=None)
def approve_event_registration(request, participation_id):
    if request.method == 'POST':
        participation = get_object_or_404(Participation, id=participation_id)
        participation.is_pending = False
        participation.is_registered = True
        participation.save()
        Operation.objects.create(
            author=request.user,
            type=OperationTypes.APPROVED_REGISTRATION.value,
            content_object=participation
        )
        return JsonResponse({'status': 'success', 'message': 'Inscription approuvée'})
    return JsonResponse({'status': 'error', 'message': 'Requête invalide'}, status=400)


@login_required
@user_passes_test(is_authorized, login_url='access_denied', redirect_field_name=None)
def reject_event_registration(request, participation_id):
    if request.method == 'POST':
        participation = get_object_or_404(Participation, id=participation_id)
        participation.is_pending = False
        participation.is_registered = False
        participation.save()
        Operation.objects.create(
            author=request.user,
            type=OperationTypes.REJECTED_REGISTRATION.value,
            content_object=participation
        )
        return JsonResponse({'status': 'success', 'message': 'Inscription rejetés'})
    return JsonResponse({'status': 'error', 'message': 'Requête invalide'}, status=400)


@login_required
@user_passes_test(is_authorized, login_url='access_denied', redirect_field_name=None)
def users(request):
    context = {
        'users': User.objects.filter(groups__name__in=['Student']).order_by('username'),
    }
    return render(request, 'dashboard/users.html', context)


@login_required
@user_passes_test(is_authorized, login_url='access_denied', redirect_field_name=None)
def stats(request):
    events_stats = {
        "inscriptions": Event.objects.filter(status="inscription").count(),
        "participations": Event.objects.filter(type="participation").count(),
    }

    return JsonResponse(events_stats)
