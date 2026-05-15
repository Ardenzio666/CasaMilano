import logging

from django.shortcuts import render

logger = logging.getLogger(__name__)

def privacy_policy(request):
    logger.info("Rendering the privacy policy page")
    return render(request, "privacy_policy.html")


def cookie_policy(request):
    logger.info("Rendering the cookie_policy page")
    return render(request, "cookie_policy.html")