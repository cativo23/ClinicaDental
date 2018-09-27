"""Sistema_Informatico_Gestion_Odontologica_Clinica_Dental_Merliot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views as SisW

urlpatterns = [
    path('GestionExpedientes/', include(('GestionExpedientes.urls', 'GestionExpedientes'), namespace='gestionExp')),
    path('', SisW.index),
    # path('', include('GestionExpedientes.urls'),),
    path('admin/', admin.site.urls),
    path('auth/', include('myauth.urls')),
    path('odo/', include(('odontograma.urls', 'odontograma'), namespace='odontograma')),
    path('django_popup_view_field/',include('django_popup_view_field.urls', namespace="django_popup_view_field")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
