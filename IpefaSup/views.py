from django.contrib.auth import authenticate
from django.shortcuts import render

from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.views.decorators.csrf import csrf_protect

from .forms import LoginForm
from datetime import datetime

@csrf_protect
def welcome(request):
    return render(request, 'welcome.html',
    {'curent_date_time': datetime.now})


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
def login_view(request):
    form = LoginForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=email, password=password)  # 🔹 Vérifie que ça retourne bien un user

            if user is not None:
                login(request, user)  # ✅ Fournir `user`
                return redirect("/welcome")
            else:
                form.add_error(None, "Identifiants invalides")  # Ajoute une erreur visible

    return render(request, "login.html", {"form": form})