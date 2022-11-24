from django.contrib import messages
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

class PerfilView(SinPrivilegios, ListView):
    permission_required="facturacion.view_cliente"
    model = Proveedor
    template_name = "compra/proveedor/perfil_proveedor.html"

    def get(self, request,id, *args, **kwargs):
        proveedor = Proveedor.objects.filter(id=id)
        enc = ComprasEnc.objects.filter(proveedor=id,pagado=True)
        context = {
            'proveedor':proveedor,
            'enc':enc,
        }
        return render(request, self.template_name, context)


class ProveedorView(SinPrivilegios, ListView):
    model = Proveedor
    template_name = "compra/proveedor/proveedor_list.html"
    context_object_name = "obj"
    permission_required="compra.view_proveedor"

class ProveedorNew(SuccessMessageMixin,SinPrivilegios,CreateView):
    model = Proveedor
    template_name = "compra/proveedor/proveedor_form.html"
    context_object_name = 'obj'
    form_class=ProveedorForm
    success_message="Proveedor Creado Correctamente"
    success_url= reverse_lazy("compra:nueva_compra")
    permission_required = "compra.add_proveedor"
    
    def post(self, request, *args, **kwargs):
        form = self.form_class()
        form_data = request.POST or None
        form_post = self.form_class(form_data)
        if request.method == 'POST':
            if 'rif' in request.POST:
                rif = request.POST['rif'].upper()
                desc = Proveedor.objects.filter(rif=rif).exists()
                if desc ==  True:
                    messages.error(request,'Ya Existe un Proveedor Registrado con Ese Rif.')
                    return redirect("compra:nueva_compra")
                else:
                    self.form_valid(form_post)
                    return redirect("compra:nueva_compra")
            return render(request, self.template_name, {'form': form})
            
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
    fail_message="Proveedor existe"
    success_url= reverse_lazy("compra:nueva_compra")
    permission_required = "compra.change_proveedor"
    
    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)


class ComprasView(SinPrivilegios, ListView):
    model = ComprasEnc
    template_name = "compra/compras/compras_list.html"
    context_object_name = "obj"
    permission_required="compra.view_comprasenc"
    
    def get(self,request):
        enc2 = ComprasEnc.objects.filter(pagado=True)
        enc = ComprasEnc.objects.filter(pagado=False)
        contexto = {'obj':enc,'obj2':enc2}
        return render(request,self.template_name,contexto)


@login_required(login_url='/login/')
@permission_required('compra.view_comprasenc', login_url='bases:sin_privilegios')
def compras(request,compra_id=None):
    template_name="compra/compras/compras.html"
    prod=Producto.objects.filter(estado=True)
    form_compras={}
    contexto={}
    if request.method=='GET':
        #codigo de facturacion
        proveedores = Proveedor.objects.filter(estado=True)
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
            fecha_compra = datetime.date.isoformat(enc.fecha_compra)
            fecha_factura = datetime.date.isoformat(enc.fecha_factura)
            e = {
                'proveedor': enc.proveedor,
                'observacion': enc.observacion,
                'no_factura': f"RM-C-{enc.id}",
                'sub_total': enc.sub_total,
                'descuento': enc.descuento,
                'total':enc.total
            }
            form_compras = ComprasEncForm(e)
        else:
            det=None
        contexto={'productos':prod,'encabezado':enc,'detalle':det,'form_enc':form_compras,"proveedores":proveedores}

    if request.method=='POST':
        fecha_compra = request.POST.get("fecha_compra")
        observacion = request.POST.get("observacion")
        no_factura = request.POST.get("no_factura")
        fecha_factura = request.POST.get("fecha_factura")
        proveedor = request.POST.get("enc_proveedor")
        sub_total = 0
        descuento = 0
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
        if producto == "":
            messages.error(request,'No ha Agregado Producto.')
            return redirect("compra:editar_compra",compra_id=compra_id)

        cantidad = request.POST.get("id_cantidad_detalle")
        precio = request.POST.get("id_precio_detalle")
        descuento_detalle  = request.POST.get("id_descuento_detalle")
        prod = Producto.objects.get(pk=producto)
        det = ComprasDet(
            compra=enc,
            producto=prod,
            cantidad=cantidad,
            precio_prv=precio,
            descuento=descuento_detalle,
            costo=0,
            uc = request.user
        )
        if det:
            det.save()
            sub_total=ComprasDet.objects.filter(compra=compra_id).aggregate(Sum('sub_total'))
            descuento=ComprasDet.objects.filter(compra=compra_id).aggregate(Sum('descuento'))
            enc.sub_total = sub_total["sub_total__sum"]
            enc.descuento=descuento["descuento__sum"]
            enc.save()
        return redirect("compra:editar_compra",compra_id=compra_id)


    return render(request, template_name, contexto)

@login_required(login_url='/login/')
@permission_required('compra.add_comprasenc', login_url='bases:sin_privilegios')
def pago_compra(request, id):
    template_name = "compra/compras/pagar_compra.html"
    enc = ComprasEnc.objects.get(pk=id)
    if request.method=="GET":
        context={"det":enc}
    if request.method == "POST":
        metodo = request.POST.get("metodo")
        monto = request.POST.get("monto")
        if metodo == "":
            return HttpResponse('No ha Seleccionado el Metodo de Pago.')
        if float(monto) < enc.total:
            return HttpResponse(f'El monto agregado para el pago es menor al total {enc.total}$')
        
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
    permission_required = "compra.delete_comprasenc"
    model = ComprasEnc
    template_name = "compra/compras/eliminar_enc.html"
    context_object_name = 'obj'
    success_message="Compra Eliminada"
    success_url= reverse_lazy("compra:lista_compras")
    
