from django import forms
from django.forms import TextInput
from .models import Medicamento, Receta, Especificacion

class nuevoMedicamentoForm(forms.ModelForm):
    class Meta:
        model = Medicamento
        fields = [
            'nombre_medicamento',
            'marca_medicamento',
            'presentacion_medicamento',
            'form_farmaceutica',
        ]
        labels = {
            'nombre_medicamento': 'Nombre del medicamento',
            'marca_medicamento': 'Marca',
            'presentacion_medicamento': 'Presentacion',
            'form_farmaceutica': 'Forma farmaceutica',
        }

        help_texts = {
            'nombre_medicamento': 'Escriba nombre del medicamento',
            'marca_medicamento': 'Escriba marca, productora o distribuidora ',
            'presentacion_medicamento': 'Ej. 100mg, 200 ml, etc',
            'form_farmaceutica': 'Ej. tabletas, pomadas, jarabe, etc',
        }


class nuevaEspecificacionForm(forms.ModelForm):
    class Meta:
        model=Especificacion
        fields = [
            'medicamento',
            'dosis',
            'duracion',
        ]

        labels = {
            'medicamento': 'Medicamento',
            'dosis': 'Dosis',
            'duracion': 'Duracion',
        }

        help_texts = {
            'medicamento': 'Medicamento',
            'dosis': 'Ej, 1 tabletas cada 6 horas',
            'duracion': 'Ej. durante 1 semana',
        }
