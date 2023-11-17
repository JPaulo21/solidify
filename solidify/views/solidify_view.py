from django.shortcuts import render, redirect
from solidify.models import ONG, Administrador
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from datetime import datetime

# Create your views here.

def login(request):
    return render(request, "solidify/login.html")