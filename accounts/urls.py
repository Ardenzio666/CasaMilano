from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('register/', views.register, name="register"),
    path('register_form/', views.register_form, name="register_form"),
    path('password_change/', views.CustomPasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', views.CustomPasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path("reset/done/",views.CustomPasswordResetDoneView.as_view(),name="password_reset_done",),
    path("reset/<uidb64>/<token>/",views.CustomPasswordResetConfirmView.as_view(),name="password_reset_confirm",),
    path("reset/complete/",views.CustomPasswordResetCompleteView.as_view(),name="password_reset_complete",),
    path("account/", views.user_management, name="user_management")
]