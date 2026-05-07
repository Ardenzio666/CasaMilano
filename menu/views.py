from django.shortcuts import redirect, render, get_object_or_404

from menu.forms import DishCommentForm
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

def add_dish_comment(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id, is_published=True)

    if request.method == "POST":
        print("Commento ricevuto")
        form = DishCommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.dish = dish
            print(f"Commento per il piatto {comment.dish}")
            if request.user.is_authenticated:
                comment.user = request.user

            comment.save()
        else:
            print(form.errors)

    return redirect("menu:menu")