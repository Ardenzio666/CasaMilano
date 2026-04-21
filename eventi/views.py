from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from .models import Event
import logging
logger = logging.getLogger(__name__)

def eventi(request):
    logger.info("Rendering EVENTI page")
    today = timezone.localdate()

    upcoming_events = Event.objects.filter(
        is_published=True,
        event_date__gte=today
    ).order_by("event_date", "order")

    past_events = Event.objects.filter(
        is_published=True,
        event_date__lt=today
    ).order_by("-event_date", "order")

    logger.info(f"Number of upcoming events: {upcoming_events.count()}")
    logger.info(f"Number of past events: {past_events.count()}")
    context = {
        "upcoming_events": upcoming_events,
        "past_events": past_events,
    }
    return render(
        request,
        'eventi.html',
        context
    )

def event_detail(request, slug):
    logger.info("Rendering the event detail page")
    try:
        event = get_object_or_404(Event, slug=slug)
    except Http404:
        logger.warning("Event not found | slug=%s", slug)
        raise

    return render(request, 'event_details.html', {
        'event': event
    })
