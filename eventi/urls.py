from django.urls import path
from . import views

app_name = 'eventi'

urlpatterns = [
    path('', views.eventi, name='eventi'),
]