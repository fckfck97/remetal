from django.shortcuts import redirect, render
from .models import ComprasEnc, ComprasDet
from django.utils import timezone, dateformat
from django.db.models import Sum
from django.contrib import messages
from django.utils.dateparse import parse_date
from datetime import timedelta

def imprimir_factura_compra(request,id):
    try:
        template_name="compra/reporte/imprimir_compra.html"
        enc = ComprasEnc.objects.get(id=id)
        det = ComprasDet.objects.filter(compra__id=id)
        if enc.monto > enc.total:
            cambio = enc.monto - enc.total
        else:
            cambio = enc.abono_monto - enc.total
            
        context={
            'request':request,
            'enc':enc,
            'detalle':det,
            'cambio':cambio
        }
        return render(request,template_name,context)
    except:
        messages.error(request,'Factura de Compra no Disponible')
        return redirect("compra:lista_compras")

def imprimir_factura_list(request,f1,f2):
    try:
        template_name="compra/reporte/facturas_compra_todas.html"
        f1=parse_date(f1)
        f2=parse_date(f2)
        f2=f2 + timedelta(days=1)

        enc = ComprasEnc.objects.filter(fecha_factura__gte=f1,fecha_factura__lt=f2,pagado=True)

        total = ComprasEnc.objects.filter(fecha_factura__gte=f1,fecha_factura__lt=f2,pagado=True).aggregate(Sum('total'))
        f2=f2 - timedelta(days=1)
        
        context = {
            'request':request,
            'f1':f1,
            'f2':f2,
            'enc':enc,
            'total':total['total__sum']
        }

        return render(request,template_name,context)
    except:
        messages.error(request,'Factura NO Disponible Intente crear una Nueva')
        return redirect("facturacion:lista_compras")


def imprimir_general_proveedor(request,id):
    try:
        template_name="compra/reporte/general_proveedor.html"
        enc = ComprasEnc.objects.filter(proveedor=id)
        total = ComprasEnc.objects.filter(proveedor=id,pagado=True).aggregate(Sum('total'))
        context={
            'request':request,
            'enc':enc,
            'total':total['total__sum']
        }
        return render(request,template_name,context)
    except:
        messages.error(request,'Factura de Compra no Disponible')
        return redirect("compra:perfil_proveedor",id=id)