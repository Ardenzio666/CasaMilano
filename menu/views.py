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
        logger.info("Comment received")
        form = DishCommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.dish = dish
            logger.info(f"Dish id for comment:  {comment.dish}")
            if request.user.is_authenticated:
                comment.user = request.user
            logger.info("Saving comment")
            comment.save()
            logger.info("Comment successfully saved")
        else:
            logger.info("Error in saving the comment to DB")
            logger.info(form.errors)

    return redirect("menu:menu")