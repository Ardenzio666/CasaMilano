from django.shortcuts import render
import logging
logger = logging.getLogger(__name__)

def dovetrovarci(request):
    logger.info("Renderign DOVETROVARCI view")
    return render(
        request,
        'dovetrovarci.html'
    )
