from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Proveedor, ComprasEnc, ComprasDet, Producto
from .forms import ProveedorForm, ComprasEncForm
from django.db.models import Sum
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from base.views import SinPrivilegios
import datetime

# Create your views here.
class ProveedorView(SinPrivilegios,ListView):
    model = Proveedor
    template_name = 'compra/proveedor/proveedor_list.html'
    context_object_name = 'obj'
    permission_required = "compra.view_proveedor"

class ProveedorNew(SuccessMessageMixin,SinPrivilegios,CreateView):
    
    model = Proveedor
    template_name = "compra/proveedor/proveedor_form.html"
    context_object_name = 'obj'
    form_class=ProveedorForm
    success_message="Proveedor Creado Correctamente"
    success_url= reverse_lazy("compra:lista_proveedores")
    permission_required = "compra.add_proveedor"

    def form_valid(self, form):
        form.instance.uc = self.request.user
        form.instance.estado = True
        return super().form_valid(form)

class ProveedorEdit(SuccessMessageMixin,SinPrivilegios,UpdateView):
    model=Proveedor
    template_name="compra/proveedor/proveedor_form.html"
    context_object_name = 'obj'
    form_class=ProveedorForm
    success_message="Proveedor Editado Correctamente"
    success_url= reverse_lazy("compra:lista_proveedores")
    permission_required = "compra.change_proveedor"
    
    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)

@login_required(login_url='/login/')
@permission_required('compra.change_proveedor', login_url='base:sin_privilegios')
def inhabilitarpro(request, id):
    proveedor = Proveedor.objects.filter(pk=id).first()

    if request.method=="POST":
        if proveedor:
            proveedor.estado = not proveedor.estado
            proveedor.save()
            return HttpResponse("OK")
        return HttpResponse("FAIL")
    
    return HttpResponse("FAIL")

class ComprasView(SinPrivilegios, ListView):
    model = ComprasEnc
    template_name = "compra/compras/compras_list.html"
    context_object_name = "obj"
    permission_required="compra.view_Encabezado_Compra"
    
    def get(self,request):
        enc2 = ComprasEnc.objects.filter(pagado=True)
        enc = ComprasEnc.objects.filter(pagado=False)
        contexto = {'obj':enc,'obj2':enc2}
        return render(request,self.template_name,contexto)


@login_required(login_url='/login/')
@permission_required('compra.view_Encabezado_Compra', login_url='bases:sin_privilegios')
def compras(request,compra_id=None):
    template_name="compra/compras/compras.html"
    prod=Producto.objects.filter(estado=True)
    form_compras={}
    contexto={}

    if request.method=='GET':
        #codigo de facturacion
        try:
            cod = ComprasEnc.objects.latest('id')
            c ={'no_factura': f"RM-C-{cod.id+1}"}
            form_compras=ComprasEncForm(c)
        except:
            cod = 0
            c ={'no_factura': f"RM-C-{cod+1}"}
            form_compras=ComprasEncForm(c)
        enc = ComprasEnc.objects.filter(pk=compra_id).first()

        if enc:
            det = ComprasDet.objects.filter(compra=enc)
            print(enc.proveedor)
            fecha_compra = datetime.date.isoformat(enc.fecha_compra)
            fecha_factura = datetime.date.isoformat(enc.fecha_factura)
            e = {
                'fecha_compra':fecha_compra,
                'proveedor': enc.proveedor,
                'observacion': enc.observacion,
                'no_factura': f"RM-C-{enc.id}",
                'fecha_factura': fecha_factura,
                'sub_total': enc.sub_total,
                'gastos_adicionales': enc.gastos_adicionales,
                'total':enc.total
            }
            form_compras = ComprasEncForm(e)
        else:
            det=None
        
        contexto={'productos':prod,'encabezado':enc,'detalle':det,'form_enc':form_compras}

    if request.method=='POST':
        fecha_compra = request.POST.get("fecha_compra")
        observacion = request.POST.get("observacion")
        no_factura = request.POST.get("no_factura")
        fecha_factura = request.POST.get("fecha_factura")
        proveedor = request.POST.get("proveedor")
        sub_total = 0
        gastos_adicionales = 0
        total = 0

        if not compra_id:
            prov=Proveedor.objects.get(pk=proveedor)

            enc = ComprasEnc(
                fecha_compra=fecha_compra,
                observacion=observacion,
                no_factura=no_factura,
                fecha_factura=fecha_factura,
                proveedor=prov,
                uc = request.user 
            )
            if enc:
                enc.save()
                compra_id=enc.id
        else:
            enc=ComprasEnc.objects.filter(pk=compra_id).first()
            if enc:
                enc.fecha_compra = fecha_compra
                enc.observacion = observacion
                enc.no_factura=no_factura
                enc.fecha_factura=fecha_factura
                enc.um=request.user.id
                enc.save()

        if not compra_id:
            return redirect("compra:lista_compras")
        
        producto = request.POST.get("id_id_producto")
        cantidad = request.POST.get("id_cantidad_detalle")
        precio = request.POST.get("id_precio_detalle")
        sub_total_detalle = request.POST.get("id_sub_total_detalle")
        gastos_adicionales_detalle  = request.POST.get("id_gastos_adicionales_detalle")
        total_detalle  = request.POST.get("id_total_detalle")

        prod = Producto.objects.get(pk=producto)

        det = ComprasDet(
            compra=enc,
            producto=prod,
            cantidad=cantidad,
            precio_prv=precio,
            gastos_adicionales=gastos_adicionales_detalle,
            costo=0,
            uc = request.user
        )

        if det:
            det.save()

            sub_total=ComprasDet.objects.filter(compra=compra_id).aggregate(Sum('sub_total'))
            gastos_adicionales=ComprasDet.objects.filter(compra=compra_id).aggregate(Sum('gastos_adicionales'))
            enc.sub_total = sub_total["sub_total__sum"]
            enc.gastos_adicionales=gastos_adicionales["gastos_adicionales__sum"]
            enc.save()

        return redirect("compra:editar_compra",compra_id=compra_id)


    return render(request, template_name, contexto)

def pago_compra(request, id):
    template_name = "compra/compras/pagar_compra.html"

    enc = ComprasEnc.objects.get(pk=id)
    if request.method=="GET":

        context={"det":enc}

    if request.method == "POST":
        metodo = request.POST.get("metodo")
        monto = request.POST.get("monto")
        enc.observacion = enc.observacion
        enc.no_factura = enc.no_factura
        enc.fecha_factura = enc.fecha_factura
        enc.total = (enc.total- float(monto))
        enc.pagado = True
        enc.tipo_pago = metodo
        enc.monto = float(monto)
        enc.user_cobra = request.user.username
        enc.save()

        return HttpResponse("ok")

        
    
    return render(request,template_name,context)



class CompraDetDelete(SinPrivilegios, DeleteView):
    permission_required = "compra.delete_comprasdet"
    model = ComprasDet
    template_name = "compra/compras/compra_eliminar.html"
    context_object_name = 'obj'
    
    def get_success_url(self):
          compra_id=self.kwargs['compra_id']
          return reverse_lazy('compra:editar_compra', kwargs={'compra_id': compra_id})


class CompraEncDelete(SinPrivilegios, DeleteView):
    permission_required = "compra.delete_Encabezado_Compra"
    model = ComprasEnc
    template_name = "compra/compras/eliminar_enc.html"
    context_object_name = 'obj'
    success_message="Compra Eliminada"
    success_url= reverse_lazy("compra:lista_compras")
    
