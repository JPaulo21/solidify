from django.shortcuts import render
from solidify.models import Voluntario
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from datetime import datetime


# Create your views here.

def home(request):
    return render(request, "voluntario/home.html")

def save_voluntario(request):

    return HttpResponseRedirect(reverse("solidify:home-adm"))