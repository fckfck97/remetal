from django import forms

from .models import Cliente


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['razon_social',
                  'tipo',
                  'rif',
                  'direccion',
                  'telefono',
                  'email']
        exclude = ['um', 'fm', 'uc', 'fc']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })    
    def clean(self):
        try:
            rif = self.cleaned_data['rif']

            if Cliente.objects.filter(rif=rif).exists():
                raise forms.ValidationError(f'Ya existe el Rif={rif}')
            return rif
        except Cliente.DoesNotExist:
            pass
        return self.cleaned_data