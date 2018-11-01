from django import forms
from django.forms import TextInput
import re


from .models import Expediente, Paciente,  Cita



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

        widgets = {'fechaNacimiento': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'datepicker'}),
                   'telefonoCasa': forms.TextInput(attrs={'class':'telefono',}),
                   'telefonoTrabajo': forms.TextInput(attrs={'class':'telefono',})
        }


class NuevaCitaForm(forms.ModelForm):

    APLICADA = 'Aplicada'
    PENDIENTE = 'Pendiente'
    NO_ASISTIO = 'No Asistio'
    ESTADO_CHOICES = (
        (APLICADA, 'Aplicada'),
        (PENDIENTE, 'Pendiente'),
        (NO_ASISTIO,'No Asistio'),
        )

    asuntoCita=forms.CharField(max_length=20, label="Asundo de Cita")
    fechaCita=forms.DateField(widget=forms.DateInput(attrs={'class':'datepicker2'}), label="Fecha Cita")
    horaCita=forms.TimeField(required=True, label="Hora de Cita")
   # observaciones=forms.CharField(max_length=20, label="observaciones")
    estado=forms.ChoiceField(choices=ESTADO_CHOICES, label="Estado Cita")


    class Meta:
        model = Cita
        fields = '__all__'

        
        
    def clean_asuntoCita(self):
                asuntoCita = self.cleaned_data.get('asuntoCita')
                if(re.match("[a-zA-Z]",asuntoCita)==None):
                    raise forms.ValidationError("El asunto de la cita debe iniciar con un caracter")
                    # "\w*" verifica que todos los caracteres sean alfanumericos # \w es lo mismo que [a-z0-9-A-Z]
                elif (re.match("\w*",asuntoCita)) ==None:
                    raise forms.ValidationError("Deben de ser caracters alfanumerico")
                return asuntoCita


