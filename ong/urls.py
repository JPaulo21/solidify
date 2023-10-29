from django.urls import path

from . import views

app_name = 'ong'

urlpatterns = [
    path("", views.index, name="index")
]
