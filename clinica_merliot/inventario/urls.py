from django.urls import path
from .views import  ProductoListView

from . import views

app_name ='inventario'

urlpatterns = [
    path('', views.index, name='home'),
    path('principalProducto/', views.ProductoListView, name = 'principalProducto'),
    path('principalProducto/agregarProducto/', views.agregarProducto, name = 'agregarProducto'),
    path('principalProducto/<pk>/edit/', views.editarProducto, name='editarProducto'),
]
