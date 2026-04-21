from django.shortcuts import render
import logging
logger = logging.getLogger(__name__)

def home_page(request):
    logger.info("rednerign HOMEPAGE")
    return render(
        request,
        'homepage/home.html',
        {
            'categories': [],
            'products': []
        }
    )