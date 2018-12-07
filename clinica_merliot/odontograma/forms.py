from django import forms
from django.forms.formsets import formset_factory
from django.forms import modelformset_factory

from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Layout, Fieldset, HTML, Field, ButtonHolder, Submit, Div
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
        self.helper.form_class = 'form-group'
        self.helper.layout = Layout(
            Fieldset(
                '',
                Div(
                    Field('notas', required="required", wrapper_class="form-group", autocomplete='off', css_class='form-control'),
                    css_class="form-group"
                    )
            ),
            ButtonHolder(
                Submit('odoform', 'Guardar', css_class='more-btn')
            )
        )
        self.fields['notas'].label = 'Observaciones: '


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
                      wrapper_class='form-control'),
                Field('cara', data_bind='value: cara',
                      wrapper_class='form-control'),
                Field('tratamiento', data_bind='value: tratamiento',
                      wrapper_class='form-control'),
                Field('diagnostico', wrapper_class='form-control'),

                Field('notas', wrapper_class='form-control')

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

        widgets = {'precioBase': forms.NumberInput(attrs={'type': 'number', 'id':'num', }),
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


class EditarProcedimientos(forms.ModelForm):
    class Meta:
        model = Procedimiento
        fields = [
                  'status',
                  ]

ProcedimientoEditFormSet = modelformset_factory(Procedimiento,fields=('status',), extra=0)
