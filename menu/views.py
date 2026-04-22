from django.shortcuts import render
from .models import Dish, Menu
import logging
logger = logging.getLogger(__name__)

def menu(request):
    logger.info("Rendering the MENU page")
    dishes = Dish.objects.filter(is_published=True)
    return render(
        request,
        'menu.html',
        {'dishes': dishes}
    )
