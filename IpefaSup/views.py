from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_protect
from datetime import datetime
from .forms import LoginForm  # Assurez-vous que LoginForm est bien impo


def welcome(request):
    return render(request, 'welcome.html', {'current_date_time': datetime.now()})  # Correction de 'curent' -> 'current' et appel de now()



@csrf_protect
def login(request):
    form = LoginForm(request.POST or None)  # Initialisation du formulaire

    if request.method == "POST" and form.is_valid():
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]
        user = authenticate(request, username=email, password=password)  # Vérifie les identifiants

        if user is not None:
            login(request, user)  # Connecte l'utilisateur
            return redirect("/welcome")  # Redirige après connexion réussie
        else:
            form.add_error(None, "Identifiants invalides")  # Affiche une erreur

    return render(request, "login.html", {"form": form})  # Affiche le formulaire