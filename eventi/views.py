from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.contrib import messages
from eventi.forms import EventCommentForm
from .models import Event
import logging
from django.contrib.auth.decorators import login_required

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

@login_required
def add_event_comment(request, event_id):
    logger.info("Entering the add_event_comment view")
    event = get_object_or_404(Event, id=event_id)

    if request.method == "POST":
        form = EventCommentForm(request.POST)

        if form.is_valid():
            logger.info("form is valid, trying to save comment")
            comment = form.save(commit=False)
            comment.event = event
            comment.user = request.user
            comment.is_approved = False
            comment.save()
            logger.info("Comment successfully saved, redirecting to event_detail")
            messages.success(
                request,
                "Commento inviato correttamente. Sarà visibile dopo approvazione."
            )
        else:
            logger.error("Form is not valid. Redirecting to event detail")
            messages.error(request, "Errore nell'invio del commento.")

    return redirect("eventi:event_detail", slug=event.slug)
