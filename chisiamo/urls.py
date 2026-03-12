from django.urls import path
from . import views

app_name = 'chisiamo'

urlpatterns = [
    path('', views.chisiamo, name='chisiamo'),
]