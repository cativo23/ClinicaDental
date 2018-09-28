from django.urls import path


from . import views

from .views import PacienteList, PacienteDetail, Paciente2List, CitaList, CitaDetail, agregarCita


urlpatterns = [
    path('', views.index, name='home'),
    path('nuevoExpediente/', views.nuevoExpediente, name='nuevoExpediente'),
    path('expedientes/', PacienteList.as_view(), name='listarExpedientes'),
    path('expedientes/<slug:id>/', PacienteDetail.as_view(), name='detalleExpediente'),
    path('actualizarExpediente/', Paciente2List.as_view(), name='listar2Expedientes'),
    path('expedientes/<pk>/edit/', views.editarExpediente, name='editarExpediente'),
    path('cita/', CitaList.as_view(), name='listarCita'),
    path('cita/<slug:id>/', views.CitaDetail.as_view(), name='detalleCita'),
    path('nuevaCita/', views.agregarCita, name='nuevaCita'),
]
