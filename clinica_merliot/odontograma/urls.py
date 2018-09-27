from django.urls import path

from . import  views

urlpatterns = [
    path('<paciente_id>/odonto/', views.odontograma, name='odontograma'),
    path('odonto/<slug:slug>/detail/', views.OdontogramaDetail.as_view(), name='odontograma_detail'),
    path('procedimientos/<slug:id>/', views.ProcedimientoDetail.as_view(), name='detalleProcedimiento'),
    path('consultas/', views.ConsultasList.as_view(), name='listarConsultas'),
    path('consultas/<slug:id>/ver/', views.ConsultaDetail.as_view(), name='detalleConsulta'),
    path('consultas/<pk>/', views.consulta, name='verConsulta'),
    path('nuevaConsulta/', views.agregarConsulta, name='nuevaConsulta'),
    path('agregarTratamiento/', views.agregarTratamiento, name='agregarTratamiento'),
    path('tratamientos/', views.TratamientoList.as_view(), name='listarTratamientos'),
    path('tratamientos/<pk>/edit/', views.editarTratamiento, name='editarTratamiento'),
    path('tratamientos/<slug:id>/', views.TratamientoDetail.as_view(), name='detalleTratamiento'),
    ]
