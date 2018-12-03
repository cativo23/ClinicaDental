from django import forms
from django.forms import TextInput, Textarea, ChoiceField
import re
from datetime import datetime

from .models import Expediente, Paciente,  Cita
from odontograma.models import Consulta



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

        widgets = {
            'observacionExp': Textarea(attrs={'cols' : 80, 'rows': 20}),
        }





class nuevoPacienteForm(forms.ModelForm):
    nombresPaciente = forms.CharField(label="Nombres del Paciente", help_text="Ingrese los nombres del paciente")
    apellidosPaciente = forms.CharField(label="Apellidos del paciente")

    class Meta:
        model = Paciente
        fields = '__all__'

        widgets = {'fechaNacimiento': forms.DateInput(format=('%d/%b/%Y'), attrs={'class':'datepicker', 'type':'text', 'id':'datepicker'}),
                   'telefonoCasa': forms.TextInput(attrs={'class':'telefono',}),
                   'telefonoTrabajo': forms.TextInput(attrs={'class':'telefono',}),
                   'sexo': forms.Select(attrs={'class':'select2_single form-control',}),
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
    fechaCita=forms.DateField(widget=forms.DateInput(attrs={'class':'datepicker'}), label="Fecha Cita")
    horaCita=forms.TimeField(required=True, label="Hora de Cita")
   # observaciones=forms.CharField(max_length=20, label="observaciones")
    estado=forms.ChoiceField(choices=ESTADO_CHOICES, label="Estado Cita")


    class Meta:
        model = Cita
        fields = '__all__'


    def clean(self):
        '''
        Revisar que el paciente no tenga cita ese dia
        '''
        cleaned_data = super(NuevaCitaForm, self).clean()
        user_exists = (Cita.objects.filter(paciente=self.cleaned_data['paciente'],fechaCita = cleaned_data.get('fechaCita')).count() > 0)

        if user_exists:
            self.add_error('fechaCita', 'El paciente ya posee una Cita en esta Fecha')

        hora_exists= (Cita.objects.filter(fechaCita=self.cleaned_data['fechaCita'],horaCita = cleaned_data.get('horaCita')).count() > 0)

        if hora_exists:
            self.add_error('horaCita', 'Esta hora ya esta reservada')



    def clean_asuntoCita(self):
                asuntoCita = self.cleaned_data.get('asuntoCita')
                if(re.match("[a-zA-Z]",asuntoCita)==None):
                    raise forms.ValidationError("El asunto de la cita debe iniciar con un caracter")
                    # "\w*" verifica que todos los caracteres sean alfanumericos # \w es lo mismo que [a-z0-9-A-Z]
                elif (re.match("\w*",asuntoCita)) ==None:
                    raise forms.ValidationError("Deben de ser caracters alfanumerico")
                return asuntoCita

class reportFecha(forms.ModelForm):
    
    fechaConsulta=forms.DateField(widget=forms.DateInput(attrs={'class':'form-control','required':True}))

    class Meta:
        model = Consulta
        fields = ['fechaConsulta']
    
        

