from django.urls import path
from . import views

app_name = 'eventi'

urlpatterns = [
    path('', views.eventi, name='eventi'),
    path('eventi/<slug:slug>/', views.event_detail, name='event_detail'),
    path("eventi/<int:event_id>/commenti/aggiungi/",views.add_event_comment,name="add_event_comment",),
]