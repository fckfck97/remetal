from datetime import datetime
from django.shortcuts import redirect, render
from .models import Producto, Gastos
from django.utils import timezone, dateformat
from django.contrib import messages
from django.db.models import Sum

def imprimir_inventario(request):
    try:
        template_name="inventario/producto/reporte_inv.html"
        today = dateformat.format(timezone.now(), 'd-m-Y')
        pro = Producto.objects.filter(estado=True)
        context={
            'request':request,
            'pro':pro,
            'hoy':today,
        }
        return render(request,template_name,context)
    except:
        messages.error(request,'Factura de Inventario no Disponible')
        return redirect("inventario:lista_productos")

def imprimir_gastos(request):
    try:
        template_name="inventario/gastos/reporte_gastos.html"
        today = dateformat.format(timezone.now(), 'd-m-Y')
        ano = dateformat.format(timezone.now(), 'Y')
        mes = dateformat.format(timezone.now(), 'm')
        pro = Gastos.objects.filter(estado=True)

        gastos = Gastos.objects.filter(fc__year=ano, fc__month=mes,estado=True).aggregate(Sum('monto_gastos'))
        if gastos['monto_gastos__sum'] is None:
            gastos['monto_gastos__sum'] = 0
        print(gastos['monto_gastos__sum'])
        context={
            'request':request,
            'pro':pro,
            'hoy':today,
            'total':gastos['monto_gastos__sum'],
            'ano':ano,
            'mes':mes,
        }
        return render(request,template_name,context)
    except:
        messages.error(request,'Factura de Gastos no Disponible')
        return redirect("inventario:lista_gastos")
