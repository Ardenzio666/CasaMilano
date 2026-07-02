import logging
from django.http import HttpResponseForbidden
from django.shortcuts import render

logger = logging.getLogger("login_debug")

def csrf_failure(request, reason=""):
    logger.warning(
        "CSRF failure",
        extra={
            "reason": reason,
            "path": request.path,
            "method": request.method,
            "host": request.get_host(),
            "is_secure": request.is_secure(),
            "referer": request.META.get("HTTP_REFERER"),
            "origin": request.META.get("HTTP_ORIGIN"),
            "user_agent": request.META.get("HTTP_USER_AGENT"),
            "cookies": list(request.COOKIES.keys()),
        },
    )
    return HttpResponseForbidden("CSRF verification failed.")