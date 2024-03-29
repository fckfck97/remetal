from unittest import mock
from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.db.models import Sum
from django.views.generic import ListView
# modelos para la grafica
from compra.models import ComprasEnc
from inventario.models import Gastos
from facturacion.models import FacturaEnc
# Create your views here.
import datetime


class SinPrivilegios(LoginRequiredMixin, PermissionRequiredMixin):
    login_url = 'base:login'
    raise_exception = False
    redirect_field_name = "redirecto_to"

    def handle_no_permission(self):
        from django.contrib.auth.models import AnonymousUser
        if not self.request.user == AnonymousUser():
            self.login_url = 'base:sin_privilegios'
        return HttpResponseRedirect(reverse_lazy(self.login_url))


class Home(LoginRequiredMixin, TemplateView):
    template_name = 'base/home.html'
    login_url = 'base:login'

    def ganancias_mes(self, mes, ano):
        compra_ganancia_mes = ComprasEnc.objects.filter(
            fecha_compra__year=ano, fecha_compra__month=mes,pagado=True).aggregate(Sum('total'))
        venta_ganancia_mes = FacturaEnc.objects.filter(
            fecha__year=ano, fecha__month=mes,pagado=True).aggregate(Sum('total'))

        if venta_ganancia_mes['total__sum'] is None:
            venta_ganancia_mes['total__sum'] = 0
        if compra_ganancia_mes['total__sum'] is None:
            compra_ganancia_mes['total__sum'] = 0

        if compra_ganancia_mes['total__sum'] > 0 and venta_ganancia_mes['total__sum'] == 0:
            total = 0
        else:
            total = venta_ganancia_mes['total__sum'] - \
                compra_ganancia_mes['total__sum']

        return total

    def ganancias_anuales(self, ano):
        compra_ganancia_ano = ComprasEnc.objects.filter(
            fecha_compra__year=ano,pagado=True).aggregate(Sum('total'))
        venta_ganancia_ano = FacturaEnc.objects.filter(
            fecha__year=ano,pagado=True).aggregate(Sum('total'))
        if venta_ganancia_ano['total__sum'] is None:
            venta_ganancia_ano['total__sum'] = 0
        if compra_ganancia_ano['total__sum'] is None:
            compra_ganancia_ano['total__sum'] = 0

        if compra_ganancia_ano['total__sum'] > 0 and venta_ganancia_ano['total__sum'] == 0:
            total_ano = 0
        else:
            total_ano = venta_ganancia_ano['total__sum'] - \
                compra_ganancia_ano['total__sum']

        return total_ano

    def get_context_data(self, **kwargs):
        # datos para la extraccion
        ano = datetime.datetime.today().year
        mes = datetime.datetime.today().month
        # gastos y descuento por mes y ano mas las ganancias por mes visualizacion calculos
        gastos = Gastos.objects.filter(
            fc__year=ano, fc__month=mes,estado=True).aggregate(Sum('monto_gastos'))
        if gastos['monto_gastos__sum'] is None:
                gastos['monto_gastos__sum'] = 0
        # visualizacion de la grafica
        context = super().get_context_data(**kwargs)
        compra_total = []
        facturacion_total = []
        gastos_total = []
        for n in range(1, 13):
            compra = ComprasEnc.objects.filter(
                fecha_compra__year=ano, fecha_compra__month=n,pagado=True).aggregate(Sum('total'))
            factura = FacturaEnc.objects.filter(
                fecha__year=ano, fecha__month=n,pagado=True).aggregate(Sum('total'))
            monto_gastos = Gastos.objects.filter(
                fc__year=ano, fc__month=n,estado=True).aggregate(Sum('monto_gastos'))
            if compra['total__sum'] is None:
                compra['total__sum'] = 0
            if factura['total__sum'] is None:
                factura['total__sum'] = 0
            if monto_gastos['monto_gastos__sum'] is None:
                monto_gastos['monto_gastos__sum'] = 0
            compra_total.append(compra['total__sum'])
            facturacion_total.append(factura['total__sum'])
            gastos_total.append(monto_gastos['monto_gastos__sum'])


        context["cenc"] = compra_total
        context["fenc"] = facturacion_total
        context["ggra"] = gastos_total
        context["total_neto"] = self.ganancias_mes(mes, ano)
        context["total_ano"] = self.ganancias_anuales(ano) - gastos['monto_gastos__sum']
        context["gastos"] = gastos['monto_gastos__sum']
        context["total"] = self.ganancias_mes(mes, ano) - gastos['monto_gastos__sum']
        return context


class HomeSinPrivilegios(LoginRequiredMixin, TemplateView):
    login_url = "base:login"
    template_name = "base/sin_privilegios.html"


class PerfilView(LoginRequiredMixin, ListView):
    #permission_required = "inv.view_categoria"
    model = User
    template_name = "base/perfil.html"

    def get(self, request, *args, **kwargs):
        context = {
            'id': self.request.user.id,
            'nombre': self.request.user.first_name,
            'apellido': self.request.user.last_name,
            'email': self.request.user.email,
            'uc': self.request.user.last_login,
            'dj': self.request.user.date_joined

        }
        return render(request, self.template_name, context)




