from django.urls import path

from . import  views

urlpatterns = [
    path('odonto/<paciente_id>', views.odontograma, name='odontograma'),
    ]
