from django.urls import path

from .views import ong_view, voluntario_view, solidify_view
from django.views.generic.base import TemplateView

app_name = 'solidify'

urlpatterns = [
    # Rota para templates abertos
    path('', TemplateView.as_view(template_name="solidify/home.html")),
    path('login/', solidify_view.login, name='login'),

    # Rota para a view relacionada à URL 'ong/'
    path('ong/', ong_view.home, name='ong_home'),
    path('ong/register/', ong_view.register_ong, name='register_ong'),
    path('ong/save_ong_adm/', ong_view.save_ong_adm, name='save_ong_adm'),
    path('home-adm/', TemplateView.as_view(template_name="ong/home-adm.html"), name='home-adm'),

    # Rota para a view relacionada à URL 'voluntario/'
    path('voluntario/', voluntario_view.home, name='voluntario_home'),
    path('ong/save_voluntario/', voluntario_view.save_voluntario, name='save_voluntario'),
]