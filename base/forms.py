from django import forms
from .models import Gastos

class GastosForm(forms.ModelForm):

    class Meta:
        model = Gastos
        fields = ['descripcion', 'monto_gastos']
        labels = {'descripcion': "Descripcion"}
        widget = {'Descripción': forms.TextInput,
                  'monto_gastos': forms.TextInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['monto_gastos'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['descripcion'].widget.attrs.update(
            {'class': 'form-control'})
