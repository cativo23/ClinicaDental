from django.urls import path
from django.conf.urls import url,include

from . import views
from .views import PacienteList, PacienteDetail, Paciente2List, CitaList, CitaDetail, agregarCita, editarCita,cita_list,prueba,ReportePacientesPDF,reporte1_crear,Reporte1

urlpatterns = [
    path('', views.index, name='home'),
    path('nuevoExpediente/', views.nuevoExpediente, name='nuevoExpediente'),
    path('expedientes/', PacienteList.as_view(), name='listarExpedientes'),
    path('expedientes/<slug:id>/', PacienteDetail.as_view(), name='detalleExpediente'),
    path('actualizarExpediente/', Paciente2List.as_view(), name='listar2Expedientes'),
    path('expedientes/<pk>/edit/', views.editarExpediente, name='editarExpediente'),
    path('cita/', CitaList.as_view(), name='listarCita'),
    path('cita/detalle/<slug:id>/', views.CitaDetail.as_view(), name='detalleCita'),
    path('nuevaCita/', views.agregarCita, name='nuevaCita'),
    path('actualizarCita/<pk>/edit/', views.editarCita, name='editarCita'),
    path('cita/Prueba/', views.cita_list, name='prueba'),
    path('cita/calendario/', views.prueba, name='calendario'),
    path('Reporte/reporte_pacientes_pdf/',ReportePacientesPDF.as_view(), name='reporte_pacientes_pdf'),
    #path('Reporte/es1/(?P<fecha>[^/]+)/(?P<fecha2>[^/]+)/', Reporte1.as_view(), name='generar_pdf_1'),
    url(r'^reporte/es1/(?P<fecha>[^/]+)/(?P<fecha2>[^/]+)/$', Reporte1.as_view(), name='generar_pdf_1'),
    path('Reporte/reporte1/',reporte1_crear, name='reporte1_crear')
]
