from django.shortcuts import redirect, render
from .models import Producto, Gastos
from django.contrib import messages
from django.db.models import Sum
from django.utils.dateparse import parse_date
from datetime import timedelta


def imprimir_todo_producto(request, f1, f2):
    try:
        template_name = "inventario/producto/total_in.html"
        f1 = parse_date(f1)
        f2 = parse_date(f2)
        f2 = f2 + timedelta(days=1)
        enc = Producto.objects.filter(
            ultima_compra__gte=f1, ultima_compra__lt=f2)
        f2 = f2 - timedelta(days=1)

        context = {
            'request': request,
            'f1': f1,
            'f2': f2,
            'enc': enc
        }
        return render(request, template_name, context)
    except:
        messages.error(
            request, 'Factura NO Disponible Intente crear una Nueva')
        return redirect("facturacion:lista_compras")


def imprimir_gastos(request, f1, f2):
    try:
        template_name = "inventario/gastos/total_gas.html"
        f1 = parse_date(f1)
        f2 = parse_date(f2)
        f2 = f2 + timedelta(days=1)
        enc = Gastos.objects.filter(
            fc__gte=f1, fc__lt=f2)
        total = Gastos.objects.filter(fc__gte=f1,fc__lt=f2).aggregate(Sum('monto_gastos'))
        f2 = f2 - timedelta(days=1)
        context = {
            'request': request,
            'f1': f1,
            'f2': f2,
            'enc': enc,
            'total':total['monto_gastos__sum'],
        }
        return render(request, template_name, context)
    except:
        messages.error(request, 'Factura de Gastos no Disponible')
        return redirect("inventario:lista_gastos")
