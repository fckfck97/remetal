from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from . import models

# Register your models here.
@admin.register(models.Categoria_Gastos)
class Categoria_Gastos(ImportExportModelAdmin):
    list_display = ('descripcion','uc',)
    search_fields = ('descripcion','uc',)