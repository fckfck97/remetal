from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from . import models

# Register your models here.
@admin.register(models.Cliente)
class Cliente(ImportExportModelAdmin):
    list_display = ('razon_social','rif',)
    search_fields = ('razon_social','rif',)


@admin.register(models.FacturaEnc)
class FacturaEnc(ImportExportModelAdmin):
    list_display = ('cliente','fecha',)
    search_fields = ('cliente','fecha',)


@admin.register(models.FacturaDet)
class FacturaDet(ImportExportModelAdmin):
    list_display = ('factura','producto',)
    search_fields = ('factura','producto',)
