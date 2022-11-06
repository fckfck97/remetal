from django.shortcuts import render
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, UpdateView,DeleteView
from .models import Categoria, Categoria_Gastos, SubCategoria, Producto, Gastos
from .forms import CategoriaForm, SubCategoriaForm, ProductoForm, GastosForm, CategoriaGastosForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse_lazy
from base.views import SinPrivilegios
#generador de codigo aleatorio

import random
# Create your views here.

#Vistas de Categoria crear, editar eliminar y ver el listadp
class CategoriaView(SinPrivilegios,ListView):
    permission_required = "inventario.view_categoria"
    model = Categoria
    template_name = "inventario/categoria/categoria_list.html"
    context_object_name = 'obj'
    
class CategoriaNew(SuccessMessageMixin,SinPrivilegios,CreateView):
    permission_required="inventario.add_categoria"
    model=Categoria
    template_name="inventario/categoria/categoria_form.html"
    context_object_name = "obj"
    form_class=CategoriaForm
    success_message="Categoria Creada Satisfactoriamente"
    success_url=reverse_lazy("inventario:lista_categoria")

    def form_valid(self, form):
        form.instance.uc = self.request.user
        form.instance.estado = True
        return super().form_valid(form)


class CategoriaEdit(SuccessMessageMixin,SinPrivilegios,UpdateView):
    permission_required="inventario.change_categoria"
    model=Categoria
    template_name="inventario/categoria/categoria_form.html"
    context_object_name = "obj"
    form_class=CategoriaForm
    success_url=reverse_lazy("inventario:lista_categoria")
    success_message="Categoria Actualizada Satisfactoriamente"

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)


@login_required(login_url='/login/')
@permission_required('inventario.change_categoria', login_url='base:sin_privilegios')
def inhabilitarcat(request, id):
    categoria = Categoria.objects.filter(pk=id).first()

    if request.method=="POST":
        if categoria:
            categoria.estado = not categoria.estado
            categoria.save()
            return HttpResponse("OK")
        return HttpResponse("FAIL")
    
    return HttpResponse("FAIL")

#Vistas de Categoria crear, editar eliminar y ver el listado


class SubCategoriaView(SinPrivilegios,ListView):
    permission_required = "inventario.view_subcategoria"
    model = SubCategoria
    template_name = "inventario/subcategoria/subcategoria_list.html"
    context_object_name = 'obj'

class SubCategoriaNew(SuccessMessageMixin,SinPrivilegios,CreateView):
    model=SubCategoria
    template_name="inventario/subcategoria/subcategoria_form.html"
    context_object_name = "obj"
    form_class=SubCategoriaForm
    success_url=reverse_lazy("inventario:lista_subcategoria")
    success_message="Sub Categoría Creada Satisfactoriamente"
    permission_required="inventario.add_subcategoria"

    def form_valid(self, form):
        form.instance.uc = self.request.user
        form.instance.estado = True
        return super().form_valid(form)


class SubCategoriaEdit(SuccessMessageMixin,SinPrivilegios, UpdateView):
    model=SubCategoria
    template_name="inventario/subcategoria/subcategoria_form.html"
    context_object_name = "obj"
    form_class=SubCategoriaForm
    success_url=reverse_lazy("inventario:lista_subcategoria")
    success_message="Sub Categoría Actualizada Satisfactoriamente"
    permission_required="inventario.change_subcategoria"

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)

@login_required(login_url='/login/')
@permission_required('inventario.change_subcategoria', login_url='base:sin_privilegios')
def inhabilitarsubcat(request, id):
    subcategoria = SubCategoria.objects.filter(pk=id).first()

    if request.method=="POST":
        if subcategoria:
            subcategoria.estado = not subcategoria.estado
            subcategoria.save()
            return HttpResponse("OK")
        return HttpResponse("FAIL")
    
    return HttpResponse("FAIL")



class ProductoView(SinPrivilegios,ListView):
    model = Producto
    template_name = "inventario/producto/producto_list.html"
    context_object_name = "obj"
    permission_required="inventario.view_producto"


class ProductoNew(SuccessMessageMixin,SinPrivilegios,CreateView):
    model=Producto
    template_name="inventario/producto/producto_form.html"
    context_object_name = 'obj'
    form_class=ProductoForm
    success_url= reverse_lazy("inventario:lista_productos")
    success_message="Producto Creado Correctamente"
    permission_required="inventario.add_producto"

    def form_valid(self, form):
        form.instance.uc = self.request.user
        form.instance.estado = True
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(ProductoNew, self).get_context_data(**kwargs)
        try:
            codigo = Producto.objects.latest('id')
            context["codigo"] = codigo.id + 1
        except:
            codigo = 0
            context["codigo"] = codigo + 1
        
        context["producto"] = Producto.objects.all()
        context["categorias"] = Categoria.objects.all()
        context["subcategorias"] = SubCategoria.objects.all()
        return context



class ProductoEdit(SuccessMessageMixin,SinPrivilegios,UpdateView):
    model=Producto
    template_name="inventario/producto/producto_form.html"
    context_object_name = 'obj'
    form_class=ProductoForm
    success_url= reverse_lazy("inventario:lista_productos")
    success_message="Producto Editado Correctamente"
    permission_required="inventario.change_producto"

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        pk = self.kwargs.get('pk')
        context = super(ProductoEdit, self).get_context_data(**kwargs)
        context["categorias"] = Categoria.objects.all()
        context["subcategorias"] = SubCategoria.objects.all()
        context["obj"] = Producto.objects.filter(pk=pk).first()
        context["codigo"] = pk

        return context


@login_required(login_url='/login/')
@permission_required('inventario.change_producto', login_url='base:sin_privilegios')
def inhabilitarproducto(request, id):
    producto = Producto.objects.filter(pk=id).first()

    if request.method=="POST":
        if producto:
            producto.estado = not producto.estado
            producto.save()
            return HttpResponse("OK")
        return HttpResponse("FAIL")
    
    return HttpResponse("FAIL")


class GastosView(SinPrivilegios,ListView):
    permission_required = "inventario.view_gastos"
    model = Gastos
    template_name = "inventario/gastos/gastos_list.html"
    context_object_name = 'obj'

class GastosNew(SuccessMessageMixin,SinPrivilegios,CreateView):
    model=Gastos
    template_name="inventario/gastos/gastos_form.html"
    context_object_name = "obj"
    form_class=GastosForm
    success_url=reverse_lazy("inventario:lista_gastos")
    success_message="Nuevo Gasto Registrado Satisfactoriamente"
    permission_required="inventario.add_gastos"

    def form_valid(self, form):
        form.instance.uc = self.request.user
        form.instance.estado = True
        return super().form_valid(form)



class GastosEdit(SuccessMessageMixin,SinPrivilegios, UpdateView):
    model=Gastos
    template_name="inventario/gastos/gastos_form.html"
    context_object_name = "obj"
    form_class=GastosForm
    success_url=reverse_lazy("inventario:lista_gastos")
    success_message="Gasto Actualizado Satisfactoriamente"
    permission_required="inventario.change_gastos"

    def form_valid(self, form):
        form.instance.estado = True
        return super().form_valid(form)

@login_required(login_url='/login/')
@permission_required('inventario.change_gastos', login_url='base:sin_privilegios')
def inhabilitargasto(request, id):
    gastos = Gastos.objects.filter(pk=id).first()
    if request.method=="POST":
        if gastos:
            gastos.estado = not gastos.estado
            gastos.save()
            return HttpResponse("OK")
        return HttpResponse("FAIL")
    
    return HttpResponse("FAIL")


#Vistas de Categoria crear, editar eliminar y ver el listadp
class Categoria_Gastos_View(SinPrivilegios,ListView):
    permission_required = "inventario.view_categoria_gastos"
    model = Categoria_Gastos
    template_name = "inventario/categoria_gastos/categoria_list.html"
    context_object_name = 'obj'
    
class Categoria_Gastos_New(SuccessMessageMixin,SinPrivilegios,CreateView):
    permission_required="inventario.add_categoria_gastos"
    model=Categoria_Gastos
    template_name="inventario/categoria_gastos/categoria_form.html"
    context_object_name = "obj"
    form_class=CategoriaGastosForm
    success_message="Categoria Creada Satisfactoriamente"
    success_url=reverse_lazy("inventario:lista_categoria_gastos")

    def form_valid(self, form):
        form.instance.uc = self.request.user
        form.instance.estado = True
        return super().form_valid(form)


class Categoria_Gastos_Edit(SuccessMessageMixin,SinPrivilegios,UpdateView):
    permission_required="inventario.change_categoria_gastos"
    model=Categoria_Gastos
    template_name="inventario/categoria_gastos/categoria_form.html"
    context_object_name = "obj"
    form_class=CategoriaGastosForm
    success_url=reverse_lazy("inventario:lista_categoria_gastos")
    success_message="Categoria Actualizada Satisfactoriamente"

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)


@login_required(login_url='/login/')
@permission_required('inventario.change_categoria_gastos', login_url='base:sin_privilegios')
def inhabilitarcatgas(request, id):
    categoria = Categoria_Gastos.objects.filter(pk=id).first()

    if request.method=="POST":
        if categoria:
            categoria.estado = not categoria.estado
            categoria.save()
            return HttpResponse("OK")
        return HttpResponse("FAIL")
    
    return HttpResponse("FAIL")