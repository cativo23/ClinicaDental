from django.urls import path


from . import views
from .views import PacienteList, PacienteDetail, TratamientoList, TratamientoDetail, Paciente2List,CitaList, CitaDetail

urlpatterns = [
    path('', views.index, name='home'),
    path('nuevoExpediente/', views.nuevoExpediente, name='nuevoExpediente'),
    path('agregarTratamiento/', views.agregarTratamiento, name='agregarTratamiento'),
    path('expedientes/', PacienteList.as_view(), name='listarExpedientes'),
    path('expedientes/<slug:id>/', PacienteDetail.as_view(), name='detalleExpediente'),
    path('tratamientos/', TratamientoList.as_view(), name='listarTratamientos'),
    path('tratamientos/<pk>/edit/', views.editarTratamiento, name='editarTratamiento'),
    path('tratamientos/<slug:id>/', TratamientoDetail.as_view(), name='detalleTratamiento'),
    path('actualizarExpediente/', Paciente2List.as_view(), name='listar2Expedientes'),
    path('consultas/', views.ConsultasList.as_view(), name='listarConsultas'),
    path('expedientes/<pk>/edit/', views.editarExpediente, name='editarExpediente'),
    path('consultas/<slug:id>/', views.ConsultaDetail.as_view(), name='detalleConsulta'),
    path('consultas/<pk>/ver/', views.consulta, name='verConsulta'),
    path('nuevaConsulta/', views.agregarConsulta, name='nuevaConsulta'),
    path('cita/', CitaList.as_view(), name='listarCita'),
    path('cita/<slug:id>/', views.CitaDetail.as_view(), name='detalleCita'),

]
