from django.shortcuts import redirect, render
from .models import Producto, Gastos
from django.utils import timezone, dateformat
from django.contrib import messages


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
        pro = Gastos.objects.filter(estado=True)
        context={
            'request':request,
            'pro':pro,
            'hoy':today,
        }
        return render(request,template_name,context)
    except:
        messages.error(request,'Factura de Gastos no Disponible')
        return redirect("inventario:lista_gastos")
