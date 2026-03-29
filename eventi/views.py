from django.shortcuts import render
from django.utils import timezone
from .models import Event

def eventi(request):
    today = timezone.localdate()

    upcoming_events = Event.objects.filter(
        is_published=True,
        event_date__gte=today
    ).order_by("event_date", "order")

    past_events = Event.objects.filter(
        is_published=True,
        event_date__lt=today
    ).order_by("-event_date", "order")

    context = {
        "upcoming_events": upcoming_events,
        "past_events": past_events,
    }
    return render(
        request,
        'eventi.html',
        context
    )
