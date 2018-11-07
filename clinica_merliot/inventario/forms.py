from django import forms
from django.forms import TextInput
from .models import Producto,  Transaccion


class nuevoProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            'nombre_producto',
            'marca_producto',
            'existencia_producto',
            'precio_producto',
        ]
        labels = {
            'nombre_producto': 'Nombre',
            'marca_producto': 'Marca o proveedor',
            'existencia_producto': 'Existencia',
            'precio_producto': 'Precio',
        }
class existenciaProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        exclude = [
            'nombre_producto',
            'marca_producto',
            'precio_producto',
        ]
        labels = {
            'existencia_producto': 'existencia',
        }


class editarProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        exclude = [
            'existencia_producto',
            'precio_producto',
        ]
        labels = {
            'nombre_producto': 'Nombre',
            'marca_producto': 'Marca o proveedor',
        }

class nuevaTransacion(forms.ModelForm):
    class Meta:
        model = Transaccion
        fields = [
            'producto',
            'tipo_transaccion',
            'cantidad',
            'fecha',
        ]

        labels = {
            'producto':'Producto',
            'tipo_transaccion':'Tipo de transaccion',
            'cantidad':'Cantidad',
            'fecha':'Fecha',
        }
