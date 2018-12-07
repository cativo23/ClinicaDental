from django import forms
from .models import Pago

class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago

        fields = [
            'cantidad',
        ]

        Labels = {
            'cantidad': 'Cantidad a Pagar',
        }

        widgets = {'cantidad': forms.NumberInput(attrs={'type': 'number', 'id':'num', }),
                   }
