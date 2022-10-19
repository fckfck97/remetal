from ast import Delete
from django.shortcuts import render,redirect
from django.views.generic import ListView, UpdateView, CreateView, DeleteView

from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from datetime import datetime
from django.contrib import messages

from django.contrib.auth import authenticate

from base.views import SinPrivilegios
from .models import Cliente, FacturaEnc, FacturaDet
from .forms import ClienteForm
from inventario.views import ProductoView
from inventario.models import Producto
class ClienteView(SinPrivilegios, ListView):
    model = Cliente
    template_name = "facturacion/clientes/lista_clientes.html"
    context_object_name = "obj"
    permission_required="facturacion.view_cliente"


class VistaBaseCreate(SuccessMessageMixin,SinPrivilegios, \
    CreateView):
    context_object_name = 'obj'
    success_message="Registro Agregado Satisfactoriamente"

    def form_valid(self, form):
        form.instance.uc = self.request.user
        form.instance.estado = True
        return super().form_valid(form)

class VistaBaseEdit(SuccessMessageMixin,SinPrivilegios, \
    UpdateView):
    context_object_name = 'obj'
    success_message="Registro Actualizado Satisfactoriamente"

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)


class ClienteNew(VistaBaseCreate):
    model=Cliente
    template_name="facturacion/clientes/cliente_form.html"
    form_class=ClienteForm
    success_url= reverse_lazy("facturacion:lista_clientes")
    permission_required="facturacion.add_cliente"

class ClienteEdit(VistaBaseEdit):
    model=Cliente
    template_name="facturacion/clientes/cliente_form.html"
    form_class=ClienteForm
    success_url= reverse_lazy("facturacion:lista_clientes")
    permission_required="facturacion.change_cliente"

    # def get(self, request, *args, **kwargs):
    #     print("sobre escribir get en editar")

    #     print(request)
        
    #     try:
    #         t = request.GET["t"]
    #     except:
    #         t = None

    #     print(t)
    #     self.object = self.get_object()
    #     form_class = self.get_form_class()
    #     form = self.get_form(form_class)
    #     context = self.get_context_data(object=self.object, form=form,t=t)
    #     print(form_class,form,context)
    #     return self.render_to_response(context)


@login_required(login_url="/login/")
@permission_required("facturacion.change_cliente",login_url="/login/")
def clienteInactivar(request,id):
    cliente = Cliente.objects.filter(pk=id).first()

    if request.method=="POST":
        if cliente:
            cliente.estado = not cliente.estado
            cliente.save()
            return HttpResponse("OK")
        return HttpResponse("FAIL")
    
    return HttpResponse("FAIL")


class FacturaView(SinPrivilegios, ListView):
    model = FacturaEnc
    template_name = "facturacion/factura/factura_list.html"
    context_object_name = "obj"
    permission_required="facturacion.view_facturaenc"

    def get_queryset(self):
        user = self.request.user
        # print(user,"usuario")
        qs = super().get_queryset()
        for q in qs:
            print(q.uc,q.id)
        
        if not user.is_superuser:
            qs = qs.filter(uc=user)

        for q in qs:
            print(q.uc,q.id)

        return qs
    def get(self,request):
        enc2 = FacturaEnc.objects.filter(pagado=True)
        enc = FacturaEnc.objects.filter(pagado=False)
        contexto = {'obj':enc,'obj2':enc2}
        return render(request,self.template_name,contexto)

@login_required(login_url='/login/')
@permission_required('facturacion.change_facturaenc', login_url='base:sin_privilegios')
def facturas(request,id=None):
    try:
        template_name='facturacion/factura/facturas.html'

        detalle = {}
        clientes = Cliente.objects.filter(estado=True)
        
        if request.method == "GET":
            enc = FacturaEnc.objects.filter(pk=id).first()
            if id:
                if not enc:
                    messages.error(request,'Factura No Existe')
                    return redirect("facturacion:lista_factura")

                usr = request.user
                if not usr.is_superuser:
                    if enc.uc != usr:
                        messages.error(request,'Factura no fue creada por usuario')
                        return redirect("facturacion:lista_factura")

            if not enc:
                encabezado = {
                    'id':0,
                    'fecha':datetime.today(),
                    'cliente':0,
                    'sub_total':0.00,
                    'descuento':0.00,
                    'total': 0.00
                }
                detalle=None
            else:
                encabezado = {
                    'id':enc.id,
                    'fecha':enc.fecha,
                    'cliente':enc.cliente,
                    'sub_total':enc.sub_total,
                    'descuento':enc.descuento,
                    'total':enc.total,
                    'pagado':enc.pagado,
                    'tipo_pago':enc.tipo_pago
                }

            detalle=FacturaDet.objects.filter(factura=enc,estado=False)
            detalle2=FacturaDet.objects.filter(factura=enc,estado=True)
            contexto = {"enc":encabezado,"det":detalle,"clientes":clientes,"det2":detalle2}
            return render(request,template_name,contexto)
        
        if request.method == "POST":
            cliente = request.POST.get("enc_cliente")
            fecha  = request.POST.get("fecha")
            cli=Cliente.objects.get(pk=cliente)

            if not id:
                enc = FacturaEnc(
                    cliente = cli,
                    fecha = fecha
                )
                if enc:
                    enc.save()
                    id = enc.id
            else:
                enc = FacturaEnc.objects.filter(pk=id).first()
                if enc:
                    enc.cliente = cli
                    enc.save()

            if not id:
                messages.error(request,'No Puedo Continuar No Pude Detectar No. de Factura')
                return redirect("facturacion:lista_factura")
            
            codigo = request.POST.get("codigo")
            cantidad = request.POST.get("cantidad")
            precio = request.POST.get("precio")
            s_total = request.POST.get("sub_total_detalle")
            descuento = request.POST.get("descuento_detalle")
            total = request.POST.get("total_detalle")

            prod = Producto.objects.get(codigo=codigo)
            det = FacturaDet(
                factura = enc,
                producto = prod,
                cantidad = cantidad,
                precio = precio,
                sub_total = s_total,
                descuento = descuento,
                total = total
            )
            
            if det:
                det.save()
            
            return redirect("facturacion:editar_factura",id=id)

        return render(request,template_name,contexto)
    except:
        messages.error(request,'Debe ingresar los Datos Correctamente')
        return redirect("facturacion:editar_factura",id=id)


class ProductoView(ProductoView):
    template_name="facturacion/factura/buscar_producto.html" 


def borrar_detalle_factura(request, id):
    template_name = "facturacion/factura/factura_borrar_detalle.html"

    det = FacturaDet.objects.get(pk=id)
    if request.method=="GET":
        context={"det":det}

    if request.method == "POST":
        usr = request.POST.get("usuario")
        pas = request.POST.get("pass")

        user =authenticate(username=usr,password=pas)

        if not user:
            return HttpResponse("Usuario o Clave Incorrecta")
        
        if not user.is_active:
            return HttpResponse("Usuario Inactivo")

        if user.is_superuser or user.has_perm("fac.sup_caja_facturadet"):
            det.id = None
            det.cantidad = (-1 * det.cantidad)
            det.sub_total = (-1 * det.sub_total)
            det.descuento = (-1 * det.descuento)
            det.total = (-1 * det.total)
            det.estado = True
            det.user_borra = request.user.username
            det.save()
            
            return HttpResponse("ok")

        return HttpResponse("Usuario no autorizado")
    
    return render(request,template_name,context)

class FacturaEncDelete(SinPrivilegios, DeleteView):
    permission_required = "compra.delete_comprasdet"
    model = FacturaEnc
    template_name = "facturacion/factura/eliminar_enc.html"
    context_object_name = 'obj'
    success_message="Compra Eliminada"
    success_url= reverse_lazy("facturacion:lista_factura")


def pago_factura(request, id):
    template_name = "facturacion/factura/pagar_factura.html"

    enc = FacturaEnc.objects.get(pk=id)
    if request.method=="GET":
        context={"det":enc}

    if request.method == "POST":
        metodo = request.POST.get("metodo")
        monto = request.POST.get("monto")
        enc.cliente = enc.cliente
        enc.pagado = True
        enc.tipo_pago = metodo
        enc.monto = float(monto)
        enc.user_cobra = request.user.username
        enc.save()
        enc = FacturaEnc.objects.get(pk=id)
        enc.pagado = True
        enc.save()
        return HttpResponse("ok")

        
    
    return render(request,template_name,context)