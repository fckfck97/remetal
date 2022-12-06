from django.shortcuts import render, redirect
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


class PerfilView(SinPrivilegios, ListView):
    permission_required="facturacion.view_cliente"
    model = Cliente
    template_name = "facturacion/clientes/perfil_cliente.html"

    def get(self, request,id, *args, **kwargs):
        cliente = Cliente.objects.filter(id=id)
        enc = FacturaEnc.objects.filter(cliente=id,pagado=True)
        context = {
            'cliente':cliente,
            'enc':enc,
        }
        return render(request, self.template_name, context)

class ClienteView(SinPrivilegios, ListView):
    model = Cliente
    template_name = "facturacion/clientes/cliente_list.html"
    context_object_name = "obj"
    permission_required="facturacion.view_cliente"


class VistaBaseCreate(SuccessMessageMixin, SinPrivilegios,
                      CreateView):
    context_object_name = 'obj'
    success_message = "Registro Agregado Satisfactoriamente"

    def form_valid(self, form):
        form.instance.uc = self.request.user
        form.instance.estado = True
        return super().form_valid(form)


class VistaBaseEdit(SuccessMessageMixin, SinPrivilegios,
                    UpdateView):
    context_object_name = 'obj'
    success_message = "Registro Actualizado Satisfactoriamente"

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)


class ClienteNew(VistaBaseCreate):
    model = Cliente
    template_name = "facturacion/clientes/cliente_form.html"
    form_class = ClienteForm
    success_url = reverse_lazy("facturacion:nueva_factura")
    permission_required = "facturacion.add_cliente"

    def post(self, request, *args, **kwargs):
        form = self.form_class()
        form_data = request.POST or None
        form_post = self.form_class(form_data)
        if request.method == 'POST':
            if 'rif' in request.POST:
                rif = request.POST['rif'].upper()
                desc = Cliente.objects.filter(rif=rif).exists()
                if desc ==  True:
                    messages.error(request,'Ya Existe un Cliente Registrado con Ese Rif.')
                    return redirect("facturacion:nueva_factura")
                else:
                    self.form_valid(form_post)
                    return redirect("facturacion:nueva_factura")
            return render(request, self.template_name, {'form': form})
    

class ClienteEdit(VistaBaseEdit):
    model = Cliente
    template_name = "facturacion/clientes/cliente_form.html"
    form_class = ClienteForm
    success_url = reverse_lazy("facturacion:nueva_factura")
    permission_required = "facturacion.change_cliente"


class FacturaView(SinPrivilegios, ListView):
    model = FacturaEnc
    template_name = "facturacion/factura/factura_list.html"
    context_object_name = "obj"
    permission_required = "facturacion.view_facturaenc"

    def get_queryset(self):
        user = self.request.user
        # print(user,"usuario")
        qs = super().get_queryset()
        for q in qs:
            print(q.uc, q.id)

        if not user.is_superuser:
            qs = qs.filter(uc=user)

        for q in qs:
            print(q.uc, q.id)

        return qs

    def get(self, request):
        enc2 = FacturaEnc.objects.filter(pagado=True)
        enc = FacturaEnc.objects.filter(pagado=False)
        contexto = {'obj': enc, 'obj2': enc2}
        return render(request, self.template_name, contexto)


@login_required(login_url='/login/')
@permission_required('facturacion.change_facturaenc', login_url='base:sin_privilegios')
def facturas(request, id=None):
    try:
        template_name = 'facturacion/factura/facturas.html'
        detalle = {}
        clientes = Cliente.objects.filter(estado=True)
        if request.method == "GET":
            enc = FacturaEnc.objects.filter(pk=id).first()
            if id:
                if not enc:
                    messages.error(request, 'Factura No Existe')
                    return redirect("facturacion:lista_factura")
                usr = request.user
                if not usr.is_superuser:
                    if enc.uc != usr:
                        messages.error(
                            request, 'Factura no fue creada por usuario')
                        return redirect("facturacion:lista_factura")
            if not enc:
                encabezado = {
                    'id': 0,
                    'fecha': datetime.today(),
                    'cliente': 0,
                    'sub_total': 0.00,
                    'descuento': 0.00,
                    'total': 0.00,
                    'guia': "",
                    'numventa':""
                }
                detalle = None
            else:
                encabezado = {
                    'id': enc.id,
                    'fecha': enc.fecha,
                    'cliente': enc.cliente,
                    'sub_total': enc.sub_total,
                    'descuento': enc.descuento,
                    'total': enc.total,
                    'guia': enc.guia,
                    'numventa': enc.numventa,
                    'pagado': enc.pagado,
                    'tipo_pago': enc.tipo_pago
                }

            detalle = FacturaDet.objects.filter(factura=enc, estado=False)
            detalle2 = FacturaDet.objects.filter(factura=enc, estado=True)

            contexto = {"enc": encabezado, "det": detalle,
                        "clientes": clientes, "det2": detalle2}
            return render(request, template_name, contexto)

        if request.method == "POST":

            cliente = request.POST.get("enc_cliente")
            fecha = request.POST.get("fecha")
            guia = request.POST.get("guia")
            numventa = request.POST.get("numventa")
            cli = Cliente.objects.get(pk=cliente)

            if not id:
                enc = FacturaEnc(
                    cliente=cli,
                    fecha=fecha,
                    guia=guia,
                    numventa=numventa
                )
                if enc:
                    enc.save()
                    id = enc.id
            else:
                enc = FacturaEnc.objects.filter(pk=id).first()
                if enc:
                    enc.cliente = cli
                    enc.guia = guia
                    enc.numventa = numventa
                    enc.save()

            if not id:
                messages.error(
                    request, 'No Puedo Continuar No Pude Detectar No. de Factura')
                return redirect("facturacion:lista_factura")

            codigo = request.POST.get("codigo")
            cantidad = request.POST.get("cantidad")
            precio = request.POST.get("precio")
            s_total = request.POST.get("sub_total_detalle")
            descuento = request.POST.get("descuento_detalle")
            total = request.POST.get("total_detalle")

            prod = Producto.objects.get(codigo=codigo)
            det = FacturaDet(
                factura=enc,
                producto=prod,
                cantidad=cantidad,
                precio=precio,
                sub_total=s_total,
                descuento=descuento,
                total=total
            )

            if det:
                
                det.save()

            return redirect("facturacion:editar_factura", id=id)

        return render(request, template_name, contexto)
    except:
        messages.error(request, 'Debe ingresar los Datos Correctamente')
        return redirect("facturacion:editar_factura", id=id)


class ProductoView(ProductoView):
    template_name = "facturacion/factura/buscar_producto.html"


def borrar_detalle_factura(request, id):
    template_name = "facturacion/factura/factura_borrar_detalle.html"

    det = FacturaDet.objects.get(pk=id)
    if request.method == "GET":
        context = {"det": det}

    if request.method == "POST":
        usr = request.POST.get("usuario")
        pas = request.POST.get("pass")
        user = authenticate(username=usr, password=pas)
        if not user:
            return HttpResponse("Usuario o Clave Incorrecta")
        if not user.is_active:
            return HttpResponse("Usuario Inactivo")
        if user.is_superuser or user.has_perm("fac.sup_caja_facturadet"):
            det.id = None
            det.cantidad = (-1 * det.cantidad)
            det.sub_total = det.sub_total
            det.descuento = (-1 * det.descuento)
            det.total = (-1 * det.total)
            det.estado = True
            det.user_borra = request.user.username
            det.save()
            return HttpResponse("ok")
        return HttpResponse("Usuario no autorizado")

    return render(request, template_name, context)


class FacturaEncDelete(SinPrivilegios, DeleteView):
    permission_required = "compra.delete_comprasdet"
    model = FacturaEnc
    template_name = "facturacion/factura/eliminar_enc.html"
    context_object_name = 'obj'
    success_message = "Compra Eliminada"
    success_url = reverse_lazy("facturacion:lista_factura")


def pago_factura(request, id):
    template_name = "facturacion/factura/pagar_factura.html"
    enc = FacturaEnc.objects.get(pk=id)
    
    if request.method == "GET":
        context = {"det": enc}
    if request.method == "POST":
        metodo = request.POST.get("metodo")
        monto = request.POST.get("monto")
        if metodo == "":
            return HttpResponse('No ha Seleccionado el Metodo de Pago.')
        if float(monto) < enc.total:
            enc.abono = True
            enc.tipo_pago = metodo
            enc.monto = float(monto)
            enc.user_cobra = request.user.username
            enc.save_abono_monto()
            return HttpResponse("ok")
        else:
            enc.pagado = True
            enc.tipo_pago = metodo
            enc.monto = float(monto)
            enc.user_cobra = request.user.username
            enc.save()

            return HttpResponse("ok")

    return render(request, template_name, context)


def desecho(request, id):
    template_name = "facturacion/factura/desecho.html"
    enc = FacturaEnc.objects.get(pk=id)
    detalle = FacturaDet.objects.filter(factura=enc,estado=False)

    if request.method == "GET":
        context = {"enc": enc, "det":detalle}
    
    if request.method == "POST":
        usr = request.POST.get("usuario")
        pas = request.POST.get("pass")
        cant = request.POST.get("cant")
        prod = request.POST.get("prod")
        det = FacturaDet.objects.get(pk=prod)
        user = authenticate(username=usr, password=pas)
        if not user:
            return HttpResponse("Usuario o Clave Incorrecta")
        if not user.is_active:
            return HttpResponse("Usuario Inactivo")
        if user.is_superuser or user.has_perm("fac.sup_caja_facturadet"):
            det.desecho = cant
            det.material_desecho()
            return HttpResponse(f"Cantidad {cant} de Desecho del Producto {prod} eliminada ")
        return HttpResponse("Usuario no autorizado")
    return render(request, template_name, context)
