from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import LoginForm
from .models import Teacher  # Vérifie que c'est bien ton modèle
from datetime import datetime


def welcome(request):
    return render(request, "welcome.html",{ 'current_date_time':datetime.now()})


def login(request):
    if len(request.POST)>0:
        form = LoginForm(request.POST)
        if form.is_valid():
            return redirect('/welcome')
        else:
            return render(request, "login.html", {'form':form})
    else:
        form = LoginForm(request.POST)
        return render(request, "login.html", {'form':form})