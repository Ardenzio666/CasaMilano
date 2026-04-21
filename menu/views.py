from django.shortcuts import render
from .models import Menu
import logging
logger = logging.getLogger(__name__)

def menu(request):
    logger.info("Rendering the MENU page")
    menus = Menu.objects.filter(is_published=True).prefetch_related('courses')
    return render(
        request,
        'menu.html',
        {'menus': menus}
    )
