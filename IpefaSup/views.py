from django.shortcuts import render

from django.shortcuts import render, redirect
from django.http import HttpRequest
from .forms import LoginForm
from datetime import datetime

def welcome(request):
    return render(request, 'welcome.html',
    {'curent_date_time': datetime.now})



def login(request: HttpRequest):
    if request.method == "GET":
        form = LoginForm(request.GET)
        if form.is_valid():
            return redirect("/welcome")
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})