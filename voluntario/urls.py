from django.urls import path

from . import views

app_name = 'voluntario'

urlpatterns = [
    path("", views.index, name="index")
]
