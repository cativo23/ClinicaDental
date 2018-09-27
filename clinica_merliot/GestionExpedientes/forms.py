from django import forms
from django.forms import TextInput
from .models import Expediente, Paciente


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

        widgets = {'fechaNacimiento': forms.DateInput(format=('%d/%m/%Y'), attrs={'class':'datepicker'}),
                   'telefonoCasa': forms.TextInput(attrs={'class':'telefono',}),
                   'telefonoTrabajo': forms.TextInput(attrs={'class':'telefono',})
        }
