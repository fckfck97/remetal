from django import forms
from .models import Categoria, SubCategoria, Producto, Gastos, Categoria_Gastos

# formulario para la vista de las categorias


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['descripcion']
        labels = {'descripcion': "Descripción de categoría"}
        widget = {'descripcion': forms.TextInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['descripcion'].widget.attrs.update(
            {'class': 'form-control'})


# formulario para la vista de las subcategorias

class SubCategoriaForm(forms.ModelForm):
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.filter(estado=True)
        .order_by('descripcion')
    )

    class Meta:
        model = SubCategoria
        fields = ['categoria', 'descripcion']
        labels = {'descripcion': "Sub Categoría"}
        widget = {'descripcion': forms.TextInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categoria'].widget.attrs.update({'class': 'form-control'})
        self.fields['descripcion'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['categoria'].empty_label = "Seleccione Categoría"


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['codigo', 'descripcion',
                  'precio', 'existencia', 'ultima_compra',
                  'subcategoria', 'foto']
        exclude = ['um', 'fm', 'uc', 'fc']
        widget = {'descripcion': forms.TextInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
        self.fields['ultima_compra'].widget.attrs['readonly'] = True
        self.fields['codigo'].widget.attrs['readonly'] = True
        self.fields['existencia'].widget.attrs['readonly'] = True
        self.fields['precio'].widget.attrs['min'] = 0


class CategoriaGastosForm(forms.ModelForm):
    class Meta:
        model = Categoria_Gastos
        fields = ['descripcion']
        labels = {'descripcion': "Descripción de categoría"}
        widget = {'descripcion': forms.TextInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['descripcion'].widget.attrs.update(
            {'class': 'form-control'})


class GastosForm(forms.ModelForm):
    categoria = forms.ModelChoiceField(
        queryset=Categoria_Gastos.objects.filter(estado=True)
        .order_by('descripcion')
    )
    fc = forms.DateInput()

    class Meta:
        model = Gastos
        fields = ['categoria', 'descripcion', 'monto_gastos','fc']
        labels = {'descripcion': "Descripcion", 'monto_gastos': 'Monto',
                  'categoria': 'Categoria', 'fc': 'Fecha'}
        widget = {'Descripción': forms.TextInput,
                  'monto_gastos': forms.NumberInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['monto_gastos'].widget.attrs.update(
            {'class': 'form-control', 'min': '0','step': '0.01'})
        self.fields['descripcion'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['categoria'].widget.attrs.update(
            {'class': 'form-select'})
        self.fields['fc'].widget.attrs.update(
            {'class': 'form-control'})

        self.fields['fc'].widget.attrs[''] = True

    def clean(self):
        try:
            sc = Gastos.objects.get(
                descripcion=self.cleaned_data["descripcion"].upper()
            )

            if not self.instance.pk:
                print("Registro ya existe")
                raise forms.ValidationError("Registro Ya Existe")
            elif self.instance.pk != sc.pk:
                print("Cambio no permitido")
                raise forms.ValidationError("Cambio No Permitido")
        except Gastos.DoesNotExist:
            pass
        return self.cleaned_data
