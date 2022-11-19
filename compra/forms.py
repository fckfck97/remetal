from django import forms
from django.shortcuts import HttpResponse
from .models import Proveedor, ComprasEnc


class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        exclude = ['um', 'fm', 'uc', 'fc']
        fields = ['razon_social',
                  'tipo',
                  'rif',
                  'direccion',
                  'direccion2',
                  'telefono',
                  'email']
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
            sc = Proveedor.objects.get(
                razon_social=self.cleaned_data["razon_social"]
            )
            if not self.instance.pk:
                print("Registro ya existe")
                raise forms.ValidationError("Registro Ya Existe")
            elif self.instance.pk!=sc.pk:
                print("Cambio no permitido")
                raise forms.ValidationError("Cambio No Permitido")
        except Proveedor.DoesNotExist:
            pass
        return self.cleaned_data
class ComprasEncForm(forms.ModelForm):
    fecha_compra = forms.DateInput()
    fecha_factura = forms.DateInput()

    class Meta:
        model = ComprasEnc
        fields = ['proveedor', 'observacion',
                  'no_factura', 'sub_total','descuento',
                  'total']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
        self.fields['no_factura'].widget.attrs['readonly'] = True
        self.fields['sub_total'].widget.attrs['readonly'] = True
        self.fields['descuento'].widget.attrs['readonly'] = True
        self.fields['total'].widget.attrs['readonly'] = True
        self.fields['observacion'].widget.attrs.update(
            {'style': 'height: calc(1.5em + 0.75rem + 2px);'})
        self.fields['proveedor'].widget.attrs.update(
            {"class": "form-select", "id": "proveedor"})
