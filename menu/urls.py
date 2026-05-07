from django.urls import path
from . import views

app_name = 'menu'

urlpatterns = [
    path('', views.menu, name='menu'),
    path(
        "piatti/<int:dish_id>/commenti/aggiungi/",
        views.add_dish_comment,
        name="add_dish_comment"
    ),
]