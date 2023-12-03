import re

from django.db.models import Q, Count
from django.shortcuts import render, redirect
from solidify.models import ONG, Administrador, Evento, Voluntarios_Evento
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from datetime import datetime
from django.utils import timezone
import pytz


# Create your views here.

def home(request):
    return render(request, "ong/home.html", )


def register_ong(request):
    return render(request, "ong/registro-ong.html")

def home_adm(request):
    usuario_id = request.session.get('adm')
    if (usuario_id):
        usuario = Administrador.objects.get(pk=usuario_id)
        prox_eventos = Evento.objects.filter(ID_ONG=usuario.ID_ONG,STATUS=True,DATA_REALIZACAO__gt=timezone.localtime(timezone.now())).order_by('DATA_REALIZACAO')

        primeiro_nome = usuario.NOME.split()
        usuario.NOME = primeiro_nome[0]

        context = {
            'usuario': usuario,
            'eventos': prox_eventos
        }

        return render(request, "ong/home-adm.html", context)
    else:
        return

def validar_ong(request):
    response_data = {
        'valido': True,
        'erros': []
    }

    if request.method == 'GET':

        cnpj = re.sub(r'[^0-9]', '', request.GET.get("cnpj"))

        cnpj_encontrado = ONG.objects.filter(CNPJ=cnpj)

        if cnpj_encontrado:
            response_data['valido'] = False
            response_data['erros'] = [{'valido': False, 'itemInvalido': 'msgErroCnpj', 'mensagem': 'CNPJ já cadastrado'}]

        return JsonResponse(response_data)

def save_ong_adm(request):
    if request.method == 'POST':
        ong = ONG()

        ong.NOME = request.POST.get("ONG_NOME")
        cnpj = re.sub(r'[^0-9]', '', request.POST.get("ONG_CNPJ"))
        ong.CNPJ = cnpj
        data_texto = request.POST.get("ONG_DT-FUNDACAO")
        ong.DATA_FUNDACAO = datetime.strptime(data_texto, '%Y-%m-%d').date()
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
        cpf = re.sub(r'[^0-9]', '', request.POST.get("ADM_CPF"))
        adm.CPF = cpf
        adm.EMAIL = request.POST.get("ADM_EMAIL")
        adm.SENHA = request.POST.get("ADM_SENHA")
        adm.ID_ONG = ong
        adm.STATUS = 1
        adm.TIPO = "A"
        adm.PRIVILEGIO = "A"

        adm.save()

        return HttpResponseRedirect(reverse("solidify:login"))

def new_event(request):
    return render(request, "ong/registro-evento-ong.html")

def save_new_event(request):
    adm_logado = request.session.get('adm')
    adm_dados = Administrador.objects.get(pk=adm_logado)

    if request.method == 'POST':
        evento = Evento()

        evento.TITULO = request.POST.get('EVENTO_TITULO')
        data_texto = request.POST.get('EVENTO_DATA_REALIZACAO')
        evento.DATA_REALIZACAO = datetime.strptime(data_texto, '%Y-%m-%d').date()
        evento.DESCRICAO = request.POST.get('EVENTO_DESCRICAO')
        evento.STATUS = True
        evento.ID_ADMINISTRADOR = adm_dados
        evento.ID_ONG = adm_dados.ID_ONG
        evento.ONG_NOME = ONG.objects.values('NOME').get(pk=adm_dados.ID_ONG.id)['NOME']
        evento.CEP = request.POST.get('E_CEP')
        evento.ENDERECO = request.POST.get('E_ENDERECO')
        evento.NUMERO = request.POST.get('E_NUMERO')
        evento.BAIRRO = request.POST.get('E_BAIRRO')
        evento.CIDADE = request.POST.get('E_CIDADE')
        evento.UF = request.POST.get('E_UF')
        evento.NR_VOLUNTARIOS = request.POST.get('NR_VOLUNTARIOS')

        evento.save()

        numeros = request.POST.getlist('numeros[]')
        cargos = request.POST.getlist('cargos[]')

        for numero, cargo_nome in zip(numeros, cargos):
            numero = int(numero)

            for _ in range(numero):
                vaga = Voluntarios_Evento()
                vaga.CARGO = cargo_nome
                vaga.ID_ONG = ONG.objects.get(pk=adm_dados.ID_ONG.id)
                vaga.ID_EVENTO = evento
                vaga.save()  # Salva o objeto no banco de dados

    return HttpResponseRedirect(reverse("solidify:home-adm"))
