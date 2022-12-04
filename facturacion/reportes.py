from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils.dateparse import parse_date
from datetime import timedelta
from django.db.models import Sum
# from django.utils.dateparse import parse_date
# from datetime import timedelta

from .models import FacturaEnc,FacturaDet

def imprimir_factura_recibo(request,id):
    try:
        template_name="facturacion/reporte/factura_ventas.html"

        enc = FacturaEnc.objects.get(id=id)
        det = FacturaDet.objects.filter(factura=id)
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
        messages.error(request,'Factura NO Disponible Intente crear una Nueva')
        return redirect("facturacion:nueva_factura")

def imprimir_factura_list(request,f1,f2):
    try:
        template_name="facturacion/reporte/factura_ventas_general.html"
        f1=parse_date(f1)
        f2=parse_date(f2)
        f2=f2 + timedelta(days=1)

        enc = FacturaEnc.objects.filter(fecha__gte=f1,fecha__lt=f2,pagado=True)
        total = FacturaEnc.objects.filter(fecha__gte=f1,fecha__lt=f2,pagado=True).aggregate(Sum('total'))
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
        return redirect("facturacion:lista_factura")


def imprimir_general_cliente(request,id):
    try:
        template_name="facturacion/reporte/general_cliente.html"
        enc = FacturaEnc.objects.filter(cliente=id)
        total = FacturaEnc.objects.filter(cliente=id,pagado=True).aggregate(Sum('total'))

        context={
            'request':request,
            'enc':enc,
            'total':total['total__sum']
        }
        return render(request,template_name,context)
    except:
        messages.error(request,'Factura NO Disponible Actualmente')
        return redirect("facturacion:perfil_cliente",id=id)


