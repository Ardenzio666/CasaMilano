from django.shortcuts import render
import logging

def chisiamo(request):
    logger = logging.getLogger(__name__)
    logger.info("RENDERING CHISIAMO PAGE")
    return render(
        request,
        'chisiamo.html'
    )
