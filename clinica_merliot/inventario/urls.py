from django.urls import path
from .views import  ProductoListView

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('principalProducto/', ProductoListView.as_view(), name = 'principalProducto'),
    path('principalProducto/agregarProducto/', views.agregarProducto, name = 'agregarProducto'),
    path('principalProducto/<pk>/edit/', views.editarProducto, name='editarProducto'),
]
