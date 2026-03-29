from django.shortcuts import render
from .models import Menu

def menu(request):
    menus = Menu.objects.filter(is_published=True).prefetch_related('courses')
    return render(
        request,
        'menu.html',
        {'menus': menus}
    )
