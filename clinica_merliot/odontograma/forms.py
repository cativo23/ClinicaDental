from django import forms
from django.forms.formsets import formset_factory

from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Layout, Fieldset, HTML, Field, ButtonHolder, Submit
)

from .models import Odontograma, Procedimiento, Tratamiento, Consulta

class OdontogramaForm(forms.ModelForm):
    class Meta:
        model = Odontograma
        exclude = ['medico', 'paciente']

    def __init__(self, *args, **kwargs):
        super(OdontogramaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Fieldset(
                '',
                Field('notas', wrapper_class='col-md-12'),
            ),
        )
        self.fields['notas'].label = 'Observaciones '

class ProcedimientoForm(forms.ModelForm):
    class Meta:
        model = Procedimiento
        exclude = ('odontograma', 'status')

    def __init__(self, *args, **kwargs):
        super(ProcedimientoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                '',
                Field('pieza', data_bind='value: diente.id',
                      wrapper_class='col-xs-1'),
                Field('cara', data_bind='value: cara',
                      wrapper_class='col-xs-2'),
                Field('tratamiento', data_bind='value: tratamiento',
                      wrapper_class='col-xs-2'),
                Field('diagnostico', wrapper_class='col-xs-2'),

                Field('notas', wrapper_class='col-xs-5')

                ),
            )


ProcedimientoFormSet = formset_factory(ProcedimientoForm, extra=0)

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
            'observacionCons',
        ]


class NuevaConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = [
            'doctor',
            'paciente',
        ]
