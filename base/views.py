from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.contrib.auth.models import User, AnonymousUser
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.db.models import Sum
# modelos para la grafica
from compra.models import ComprasEnc
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
            fecha_compra__year=ano, fecha_compra__month=mes).aggregate(Sum('total'))
        venta_ganancia_mes = FacturaEnc.objects.filter(
            fecha__year=ano, fecha__month=mes).aggregate(Sum('total'))

        if venta_ganancia_mes['total__sum'] is None:
            venta_ganancia_mes['total__sum'] = 0
        if compra_ganancia_mes['total__sum'] is None:
            compra_ganancia_mes['total__sum'] = 0

        total = venta_ganancia_mes['total__sum'] - \
            compra_ganancia_mes['total__sum']
        if total is None:
            total = 0
        return total

    def ganancias_anuales(self, ano):
        compra_ganancia_ano = ComprasEnc.objects.filter(
            fecha_compra__year=ano).aggregate(Sum('total'))
        venta_ganancia_ano = FacturaEnc.objects.filter(
            fecha__year=ano).aggregate(Sum('total'))
        if venta_ganancia_ano['total__sum'] is None:
            venta_ganancia_ano['total__sum'] = 0
        if compra_ganancia_ano['total__sum'] is None:
            compra_ganancia_ano['total__sum'] = 0

        total_ano = compra_ganancia_ano['total__sum'] - venta_ganancia_ano['total__sum']
        
        if total_ano is None:
            total_ano = 0
        return total_ano

    def get_context_data(self, **kwargs):
        # datos para la extraccion
        ano = datetime.datetime.today().year
        mes = datetime.datetime.today().month
        # gastos y descuento por mes y ano mas las ganancias por mes visualizacion calculos
        gastos = ComprasEnc.objects.filter(
            fecha_compra__year=ano, fecha_compra__month=mes).aggregate(Sum('gastos_adicionales'))
        descuento = FacturaEnc.objects.filter(
            fecha__year=ano, fecha__month=mes).aggregate(Sum('descuento'))

        # visualizacion de la grafica
        context = super().get_context_data(**kwargs)
        compra_total = []
        facturacion_total = []
        for n in range(1, 13):
            compra = ComprasEnc.objects.filter(
                fecha_compra__year=ano, fecha_compra__month=n).aggregate(Sum('total'))
            factura = FacturaEnc.objects.filter(
                fecha__year=ano, fecha__month=n).aggregate(Sum('total'))
            if compra['total__sum'] is None:
                compra['total__sum'] = 0
            if factura['total__sum'] is None:
                factura['total__sum'] = 0
            compra_total.append(compra['total__sum'])
            facturacion_total.append(factura['total__sum'])
        diferencia = [e1 - e2 for e1,
                      e2 in zip(facturacion_total,compra_total)]
        print(diferencia)
        context["cenc"] = compra_total
        context["fenc"] = facturacion_total
        context["ganancias_mes"] = diferencia
        context["total"] = self.ganancias_mes(mes, ano)
        context["total_ano"] = self.ganancias_anuales(ano)
        context["gastos"] = gastos['gastos_adicionales__sum']
        context["descuento"] = descuento['descuento__sum']
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
