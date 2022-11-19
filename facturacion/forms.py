from django import forms

from .models import Cliente


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['razon_social',
                  'tipo',
                  'rif',
                  'direccion',
                  'direccion2',
                  'telefono',
                  'email']
        exclude = ['um', 'fm', 'uc', 'fc']
        labels = {'direccion': "Direccion Principal", 'direccion2': "Direccion Secundaria(Opcional)",
                  'telefono': "Numero Telefonico", 'email': "Correo Electronico"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    def clean(self):
        try:
            sc = Cliente.objects.get(
                razon_social=self.cleaned_data["razon_social"].upper()
            )
            if not self.instance.pk:
                print("Registro ya existe")
                raise forms.ValidationError("Registro Ya Existe")
            elif self.instance.pk != sc.pk:
                print("Cambio no permitido")
                raise forms.ValidationError("Cambio No Permitido")
        except Cliente.DoesNotExist:
            pass
        return self.cleaned_data
