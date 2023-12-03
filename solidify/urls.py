from django.urls import path

from .views import ong_view, voluntario_view, solidify_view
from django.views.generic.base import TemplateView

app_name = 'solidify'

urlpatterns = [
    # Rota para templates abertos
    path('', TemplateView.as_view(template_name="solidify/home.html")),
    path('login/', solidify_view.login, name='login'),
    path('logar/', solidify_view.logar, name='logar'),
    path('logout/', solidify_view.logout, name='logout'),
    path('endereco/', solidify_view.buscar_endereco, name='buscar_endereco'),
    path('validar/usuario/', solidify_view.validar_usuario, name='validar-usuario'),
    path('validar/login/', solidify_view.validar_login, name='validar-usuario'),

    # Rota para a view relacionada à URL 'ong/'
    path('ong/', ong_view.home, name='ong_home'),
    path('ong/register/', ong_view.register_ong, name='register_ong'),
    path('ong/save_ong_adm/', ong_view.save_ong_adm, name='save_ong_adm'),
    path('ong/home-adm/', ong_view.home_adm, name='home-adm'),
    path('ong/new-event/', ong_view.new_event, name='new-event'),
    path('validar/ong/', ong_view.validar_ong, name='validar-ong'),
    path('ong/save-new-event/', ong_view.save_new_event, name='save-new-event'),

    # Rota para a view relacionada à URL 'voluntario/'
    path('voluntario/', voluntario_view.home, name='voluntario_home'),
    path('voluntario/home-voluntario', voluntario_view.home_voluntario, name='home-voluntario'),
    path('voluntario/register', voluntario_view.register_voluntario, name='register-voluntario'),
    path('voluntario/save_voluntario/', voluntario_view.save_voluntario, name='save-voluntario'),
    path('voluntario/evento/<int:id_evento>/', voluntario_view.participar_evento, name='participar-evento'),
    path('voluntario/save_participacao/', voluntario_view.save_participacao, name='save-participacao'),
    path('voluntario/retirar_participacao/', voluntario_view.retirar_participacao, name='retirar-participacao'),

]