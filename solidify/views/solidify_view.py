from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from solidify.models import Usuario, Voluntario, ONG
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.urls import reverse
from datetime import datetime
import re
import requests

# Create your views here.

def login(request):
    return render(request, "solidify/login.html")

def logar(request):
    if request.method == 'POST':
        try:
            usuario = Usuario()

            cpf = cpf = re.sub(r'[^0-9]', '', request.POST.get("USUARIO_CPF"))
            usuario.CPF = cpf
            usuario.SENHA = request.POST.get("USUARIO_SENHA")

            usuario_encontrado = get_object_or_404(Usuario,CPF=usuario.CPF, SENHA=usuario.SENHA, STATUS=True)

            print(usuario_encontrado.CPF)
            print(usuario_encontrado.TIPO)
            print(usuario_encontrado.STATUS)
            if usuario_encontrado and usuario_encontrado.TIPO == 'V':
                request.session['voluntario'] = usuario_encontrado.id
                request.session['autenticado_voluntario'] = 'S'
                return HttpResponseRedirect(reverse("solidify:home-voluntario"))
            if usuario_encontrado and usuario_encontrado.TIPO == 'A':
                request.session['adm'] = usuario_encontrado.id
                request.session['autenticado_adm'] = 'S'
                return HttpResponseRedirect(reverse("solidify:home-adm"))

        except ObjectDoesNotExist:
            return 1


def logout(request):
    request.session.clear()
    return redirect('/')

# -------------------------------------------------------------------------

def validar_usuario(request):
    response_data = {
        'valido': True,
        'erros': []
    }

    if request.method == 'GET':
        voluntario = Voluntario()
        voluntario.EMAIL = request.GET.get("email")
        voluntario.CPF = request.GET.get("cpf")

        cpf = re.sub(r'[^0-9]', '', voluntario.CPF)

        cpf_encontrado = Usuario.objects.filter(CPF=cpf)
        email_encontrado = Usuario.objects.filter(EMAIL=voluntario.EMAIL)

        if cpf_encontrado:
            response_data['valido'] = False
            response_data['erros'] = [{'valido': False, 'itemInvalido': 'msgErroCpf', 'mensagem': 'CPF já cadastrado'}]
        if email_encontrado:
            response_data['valido'] = False
            response_data['erros'].append({'valido': False, 'itemInvalido': 'msgErroEmail', 'mensagem': 'E-mail já cadastrado'})

        return JsonResponse(response_data)

#--------------------------------------------------------------------------
def buscar_endereco(request):
    dados_endereco = {
        'endereco': '',
        'bairro': '',
        'cidade': '',
        'uf': ''
    }

    if request.method == 'GET':
        cepFormatada = request.GET.get("cep")

        cep = re.sub(r'[^0-9]', '', cepFormatada)
        url = f'https://viacep.com.br/ws/{cep}/json/'
        response = requests.get(url)
        dados = response.json()

        dados_endereco['endereco'] = dados['logradouro']
        dados_endereco['bairro'] = dados['bairro']
        dados_endereco['cidade'] = dados['localidade']
        dados_endereco['uf'] = dados['uf']

        return JsonResponse(dados_endereco)


def validar_login(request):
    response_data = {
        'valido': True,
        'erros': []
    }

    if request.method == 'GET':

        if request.GET.get("cpf") is None:
            print('tá nulo')

        cpf = re.sub(r'[^0-9]', '', request.GET.get("cpf"))
        senha = request.GET.get("senha")

        cpf_encontrado = Usuario.objects.filter(CPF=cpf, SENHA=senha).first()

        if cpf_encontrado is None:
            response_data['valido'] = False
            response_data['erros'] = [{'valido': False, 'itemInvalido': 'msgErro', 'mensagem': 'login inválido'}]

        return JsonResponse(response_data)
