from django import forms
from django.forms import TextInput


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
    nombresPaciente = forms.CharField(label="Nombres del Paciente", help_text="Ingrese los nombres del paciente")
    apellidosPaciente = forms.CharField(label="Apellidos del paciente")

    class Meta:
        model = Paciente
        fields = '__all__'

        widgets = {'fechaNacimiento': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'datepicker'}),
                   'telefonoCasa': forms.TextInput(attrs={'class':'telefono',}),
                   'telefonoTrabajo': forms.TextInput(attrs={'class':'telefono',})
        }


class NuevaCitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = [
            'asuntoCita',
            'doctor',
            'paciente',
            'fechaCita',
            'horaCita',
            'observacionCita',
            'estado',
        ]

        labels = {
            'asuntoCita': 'Asunto de la Cita',
            'doctor': 'Doctor Asignado',
            'paciente': 'Nombre Paciente',
            'fechaCita': 'Fecha de proxima cita',
            'horaCita': 'Hora de Cita',
            'observacionCita': 'Observaciones',
            'estado': 'Estado de la cita',
        }

        widgets = {'fechaCita': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'datepicker'}),}
