from django import forms
from .models import Categoria, SubCategoria, Producto

#formulario para la vista de las categorias

class CategoriaForm(forms.ModelForm):
    class Meta:
        model=Categoria
        fields = ['descripcion']
        labels = {'descripcion':"Descripción de categoría"}
        widget={'descripcion': forms.TextInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.fields['descripcion'].widget.attrs.update({'class':'form-control'})
       

#formulario para la vista de las subcategorias

class SubCategoriaForm(forms.ModelForm):
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.filter(estado=True)
        .order_by('descripcion')
    )
    class Meta:
        model=SubCategoria
        fields = ['categoria','descripcion']
        labels = {'descripcion':"Sub Categoría"}
        widget={'descripcion': forms.TextInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.fields['categoria'].widget.attrs.update({'class':'form-control'})
        self.fields['descripcion'].widget.attrs.update({'class':'form-control'})
        self.fields['categoria'].empty_label =  "Seleccione Categoría"

class ProductoForm(forms.ModelForm):
    class Meta:
        model=Producto
        fields=['codigo','descripcion', \
                'precio','existencia','ultima_compra',
                'subcategoria','foto']
        exclude = ['um','fm','uc','fc']
        widget={'descripcion': forms.TextInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
        self.fields['ultima_compra'].widget.attrs['readonly'] = True
        self.fields['codigo'].widget.attrs['readonly'] = True
        self.fields['existencia'].widget.attrs['readonly'] = True