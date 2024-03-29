from django import forms
from .models import Categoria, SubCategoria, Producto, Gastos

# formulario para la vista de las categorias


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['title','descripcion']
        labels = {'title':'Tipo de Categoria','descripcion': "Descripción de categoría"}
        widget = {'descripcion': forms.TextInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['descripcion'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['title'].widget.attrs.update(
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


class GastosForm(forms.ModelForm):
    fc = forms.DateInput()

    class Meta:
        model = Gastos
        fields = ['subcategoria', 'descripcion', 'monto_gastos','fc']
        labels = {'descripcion': "Descripcion", 'monto_gastos': 'Monto',
                  'subcategoria': 'SubCategoria', 'fc': 'Fecha'}
        widget = {'Descripción': forms.TextInput,
                  'monto_gastos': forms.NumberInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['monto_gastos'].widget.attrs.update(
            {'class': 'form-control', 'min': '0','step': '0.01'})
        self.fields['descripcion'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['subcategoria'].widget.attrs.update(
            {'class': 'form-select'})
        self.fields['fc'].widget.attrs.update(
            {'class': 'form-control'})

        self.fields['descripcion'].widget.attrs["required"] = "required"

    