from django.shortcuts import render, redirect
from solidify.models import ONG, Administrador
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from datetime import datetime


# Create your views here.

def home(request):
    return render(request, "ong/home.html", )


def register_ong(request):
    return render(request, "ong/register-ong.html")


def save_ong_adm(request):
    if request.method == 'POST':
        ong = ONG()

        ong.NOME = request.POST.get("ONG_NOME")
        ong.CNPJ = request.POST.get("ONG_CNPJ")
        data_texto = request.POST.get("ONG_DT-FUNDACAO")
        ong.DATA_FUNDACAO = datetime.strptime(data_texto, '%d/%m/%Y').date()
        ong.STATUS = 1
        ong.CEP = request.POST.get("ONG_CEP")
        ong.ENDERECO = request.POST.get("ONG_ENDERECO")
        ong.NUMERO = request.POST.get("ONG_NUMERO")
        ong.BAIRRO = request.POST.get("ONG_BAIRRO")
        ong.CIDADE = request.POST.get("ONG_CIDADE")
        ong.UF = request.POST.get("ONG_UF")

        ong.save()

        adm = Administrador()
        adm.NOME = request.POST.get("ADM_NOME")
        adm.CPF = request.POST.get("ADM_CPF")
        adm.EMAIL = request.POST.get("ADM_EMAIL")
        adm.SENHA = request.POST.get("ADM_SENHA")
        adm.ID_ONG = ong
        adm.STATUS = 1
        adm.PRIVILEGIO = "A"

        adm.save()

        return HttpResponseRedirect(reverse("solidify:home-adm"))
