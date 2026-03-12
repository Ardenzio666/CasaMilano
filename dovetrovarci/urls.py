from django.urls import path
from . import views

app_name = 'dovetrovarci'

urlpatterns = [
    path('', views.dovetrovarci, name='dovetrovarci'),
]