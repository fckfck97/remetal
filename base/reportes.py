from django.contrib import messages
from django.shortcuts import redirect, render
from django.db.models import Sum
import datetime
from compra.models import ComprasEnc
from inventario.models import Gastos
from facturacion.models import FacturaEnc




def imprimir_general_empresa(request):
    try:
        template_name="base/reporte_general.html"
        ano = datetime.datetime.today().year
        mes = datetime.datetime.today().month
        #Ganancias y Perdidas mes actual
        compra_ganancia_mes = ComprasEnc.objects.filter(
            fecha_compra__year=ano, fecha_compra__month=11,pagado=True).aggregate(Sum('total'))
        venta_ganancia_mes = FacturaEnc.objects.filter(
            fecha__year=ano, fecha__month=11,pagado=True).aggregate(Sum('total'))

        if venta_ganancia_mes['total__sum'] is None:
            venta_ganancia_mes['total__sum'] = 0
        if compra_ganancia_mes['total__sum'] is None:
            compra_ganancia_mes['total__sum'] = 0

        if compra_ganancia_mes['total__sum'] > 0 and venta_ganancia_mes['total__sum'] == 0:
            total = 0
        else:
            total = venta_ganancia_mes['total__sum'] - \
                compra_ganancia_mes['total__sum']
        #Gastos????????????????????????????????????????
        gastos = Gastos.objects.filter(
            fc__year=ano, fc__month=11,estado=True).aggregate(Sum('monto_gastos'))
        if gastos['monto_gastos__sum'] is None:
                gastos['monto_gastos__sum'] = 0
    
        context={
            'request':request,
            'total_neto':total,
            'gastos':gastos['monto_gastos__sum'],
            'total': total - gastos['monto_gastos__sum'],
            'mes':mes,
            'ano':ano,
            'compra':compra_ganancia_mes['total__sum'],
            'venta':venta_ganancia_mes['total__sum']
        }
        return render(request,template_name,context)
    except:
        messages.error(request,'Factura NO Disponible Actualmente')
        return redirect("facturacion:perfil_cliente",id=id)
