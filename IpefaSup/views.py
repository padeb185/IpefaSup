from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_protect
from django.http import HttpRequest
from datetime import datetime
from .forms import LoginForm  # Assurez-vous que LoginForm est bien impo


def welcome(request: HttpRequest):
    return render(request, 'welcome.html', {'current_date_time': datetime.now()})  # Correction de 'curent' -> 'current' et appel de now()

@csrf_protect
def login(request: HttpRequest):
    if request.method == "GET":
        form = LoginForm(request.GET)
        if form.is_valid():
            return redirect("/welcome")
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})

@csrf_protect
def login_view(request: HttpRequest):
    form = LoginForm(request.POST or None)

    if request.method == "POST" and form.is_valid():  # Vérifie validité uniquement en POST
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect("/welcome")
        else:
            form.add_error(None, "Identifiants invalides")

    return render(request, "login.html", {"form": form})
