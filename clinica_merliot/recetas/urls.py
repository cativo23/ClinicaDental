from django.urls import path

from . import views
from .views import  principalRecetas, principalMedicamento

app_name ='rec'

urlpatterns = [
    path('', views.principalRecetas, name='pRecetas'),
    path('medicamentos/', views.principalMedicamento, name='pMedicamentos'),
    path('asignarReceta/', views.asignandoReceta, name='aRecetas'),
]
