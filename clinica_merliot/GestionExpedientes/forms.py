from django import forms
from django.forms import TextInput
from .models import Expediente, Paciente, Tratamiento, Consulta


class ExpForm(forms.ModelForm):
    class Meta:
        model = Expediente

        fields = [
            'observacionExp'
        ]


class nuevoExpedienteForm(forms.ModelForm):
    class Meta:
        model = Expediente

        exclude = [
            'paciente',
            'fechaCreacion',
            'pagado',
            'saldo',
        ]

        labels = {
            'tratamientos': 'Tratamientos',
            'fechaCreacion': 'Fecha de Creación',
            'pagado': 'Saldo pagado',
        }

        help_texts = {
            'tratamientos': 'Mantenga presionado "Ctrl" o "Command" , para seleccionar más de una opción.'
        }




class nuevoPacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = '__all__'


class nuevoTratamientoForm(forms.ModelForm):
    class Meta:
        model = Tratamiento
        fields = [
            'nombreTratamiento',
            'descripcionTratamiento',
            'precioBase',
        ]
        labels = {
            'nombreTratamiento': 'Nombre del Tratamiento',
            'descripcionTratamiento': 'Descripcion',
            'precioBase': 'Precio Base',
        }


class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = [
            'doctor',
            'observacionCons'
        ]


class NuevaConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = [
            'doctor',
            'paciente',
            'observacionCons',
        ]
