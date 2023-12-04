from django.db.models import Count, When, F, Q
from django.shortcuts import redirect, render
from solidify.models import Voluntario, Usuario, Evento, Voluntarios_Evento, ONG
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from datetime import datetime
import re
from django.utils import timezone
from colorama import Fore, Style


# Create your views here.

def home(request):
    return render(request, "voluntario/home.html")

def home_voluntario(request):
    usuario_id = request.session.get('voluntario')
    eventos_voluntario_inscrito = []
    if(usuario_id):
        voluntario = Voluntario.objects.get(pk=usuario_id)
        primeiro_nome = voluntario.NOME.split()
        voluntario.NOME = primeiro_nome[0]
        
        eventos_estado = Evento.objects.filter(UF=voluntario.UF,STATUS=True,DATA_REALIZACAO__gt=timezone.localtime(timezone.now())).order_by('DATA_REALIZACAO')
        eventos_para_participar = eventos_estado
        for evento in eventos_para_participar:
            print(f'{Fore.GREEN}Evento: {evento}{Style.RESET_ALL}')
            voluntario_participa_evento = Voluntarios_Evento.objects.filter(ID_EVENTO=evento, ID_VOLUNTARIO=voluntario).first()
            print(f'{Fore.GREEN}voluntario_participa_evento: {voluntario_participa_evento}{Style.RESET_ALL}')
            if voluntario_participa_evento:
                eventos_para_participar = eventos_para_participar.exclude(pk=voluntario_participa_evento.ID_EVENTO.id)

            print(f'{Fore.GREEN}Eventos que o voluntario não está escrtio {eventos_para_participar}{Style.RESET_ALL}')

        for evento in eventos_estado:
            voluntario_participa_evento = Voluntarios_Evento.objects.filter(ID_EVENTO=evento, ID_VOLUNTARIO=voluntario).first()
            if voluntario_participa_evento:
                eventos_voluntario_inscrito.append(evento)
                print(f'Eventos: {evento}')

        context = {
            'eventos': eventos_para_participar,
            'voluntario': voluntario,
            'eventos_inscrito': eventos_voluntario_inscrito
        }
        return render(request, "voluntario/home-voluntario.html", context)
    else:
        return

def register_voluntario(request):
    return render(request, "voluntario/registro-voluntario.html")

def save_voluntario(request):
    if request.method == 'POST':
        voluntario = Voluntario()

        voluntario.NOME = request.POST.get("V_NOME")
        cpf = re.sub(r'[^0-9]', '', request.POST.get("V_CPF"))
        voluntario.CPF = cpf
        data_texto = request.POST.get("V_DT-NASC")
        voluntario.DATA_NASC = datetime.strptime(data_texto, '%Y-%m-%d').date()
        voluntario.EMAIL = request.POST.get("V_EMAIL")
        voluntario.SENHA = request.POST.get("V_SENHA")
        voluntario.STATUS = 1
        voluntario.TIPO = 'V'
        voluntario.CEP = request.POST.get("V_CEP")
        voluntario.ENDERECO = request.POST.get("V_ENDERECO")
        voluntario.NUMERO = request.POST.get("V_NUMERO")
        voluntario.BAIRRO = request.POST.get("V_BAIRRO")
        voluntario.CIDADE = request.POST.get("V_CIDADE")
        voluntario.UF = request.POST.get("V_UF")

        voluntario.save()

        return HttpResponseRedirect(reverse("solidify:login"))

def participar_evento(request, id_evento):
    evento = Evento.objects.get(pk=id_evento)
    evento.DATA_REALIZACAO = evento.DATA_REALIZACAO.strftime("%d/%m/%Y")
    usuario_id = request.session.get('voluntario')
    print(usuario_id)
    voluntario = Voluntario.objects.get(pk=usuario_id)
    print(voluntario)


    vagas = (Voluntarios_Evento.objects.filter(ID_EVENTO=evento)
             .values('CARGO')
             .annotate(TOTAL=Count('CARGO'),
                        OCUPADAS=Count('ID_VOLUNTARIO', filter=Q(ID_VOLUNTARIO__isnull=False)))
             .annotate(VAGAS_DISPONIVEIS=F('TOTAL') - F('OCUPADAS'))
             )

    context = {
        'voluntario': voluntario,
        'evento': evento,
        'vagas': vagas
    }

    return render(request, "voluntario/participar-evento-voluntario.html", context)

def save_participacao(request):
    if (request.method == 'POST'):
        cargo = request.POST.get('vaga_cargo')
        inscrito = Voluntarios_Evento.objects.filter(CPF_VOLUNTARIO__isnull=True, CARGO=cargo).first()

        evento = inscrito.ID_EVENTO
        evento.NR_OCUPADOS += 1
        evento.save()

        inscrito.CPF_VOLUNTARIO = request.POST.get('vaga_cpf')
        voluntario = Voluntario.objects.get(pk=request.POST.get('vaga_voluntario'))
        inscrito.ID_VOLUNTARIO = voluntario
        evento = Evento.objects.get(pk=request.POST.get('vaga_evento'))
        inscrito.ID_EVENTO = evento
        ong = ONG.objects.get(pk=request.POST.get('vaga_ong'))
        inscrito.ID_ONG = ong
        inscrito.NOME = request.POST.get('vaga_nome')

        inscrito.save()

    return HttpResponseRedirect(reverse("solidify:home-voluntario"))

def retirar_participacao(request):
    if (request.method == 'POST'):
        evento = Evento.objects.get(pk=request.POST.get('evento_id'))
        voluntario = Voluntario.objects.get(pk=request.POST.get('volunt_id'))
        vaga = Voluntarios_Evento.objects.filter(ID_VOLUNTARIO = voluntario, ID_EVENTO=evento).first()

        vaga.ID_VOLUNTARIO = None
        vaga.NOME = None
        vaga.CPF_VOLUNTARIO = None

        vaga.save()

        nr_participantes = Voluntarios_Evento.objects.filter(ID_EVENTO=evento, ID_VOLUNTARIO_id__isnull=False).count()
        print(f'{Fore.RED}Nº de vagas ocupadas pegando da tabela de vagas: {nr_participantes}{Style.RESET_ALL}')
        evento.NR_OCUPADOS = nr_participantes
        print(f'Nº de vagas ocupadas pegando da tabela de vagas: {nr_participantes}')

        evento.save()

        return HttpResponseRedirect(reverse("solidify:home-voluntario"))
    
    return redirect(reverse("solidify:home-voluntario")) 

