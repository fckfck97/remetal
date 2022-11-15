from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from . import models

# Register your models here.
@admin.register(models.Proveedor)
class Proveedor(ImportExportModelAdmin):
    list_display = ('razon_social','rif',)
    search_fields = ('razon_social','rif',)


@admin.register(models.ComprasEnc)
class ComprasEnc(ImportExportModelAdmin):
    list_display = ('observacion','no_factura',)
    search_fields = ('observacion','no_factura',)


@admin.register(models.ComprasDet)
class ComprasDet(ImportExportModelAdmin):
    list_display = ('compra','producto',)
    search_fields = ('compra','producto',)