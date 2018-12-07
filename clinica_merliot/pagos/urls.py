from django.urls import path

from . import  views

urlpatterns = [
    path('pago/<id>/', views.agregarPago, name='agregarPago')
]
