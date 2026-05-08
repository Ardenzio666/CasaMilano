from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .forms import LoginForm
import logging

logger = logging.getLogger(__name__)

def user_login(request):
    if request.method == 'POST':
        logger.info("Auth request received")
        form = LoginForm(request.POST)
        if form.is_valid():
            cf = form.cleaned_data
            user_record = None
            try:
                user_record = User.objects.get(email=cf['email'])
                logger.info(f"User with email {user_record} is trying to authenticate")
            except User.DoesNotExist:
                pass
            if user_record:
                user = authenticate(
                    request,
                    username=user_record,
                    password=cf['password']
                )
                if user is not None:
                    login(request, user)
                    logger.info("User is successfully authenticated")
                    return redirect('homepage:home')
            messages.error(request, 'Incorrect email / password')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})