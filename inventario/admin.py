from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from . import models

# Register your models here.
@admin.register(models.Categoria)
class Categoria(ImportExportModelAdmin):
    list_display = ('descripcion','uc',)
    search_fields = ('descripcion','uc',)


@admin.register(models.SubCategoria)
class SubCategoria(ImportExportModelAdmin):
    list_display = ('descripcion','uc',)
    search_fields = ('descripcion','uc',)

@admin.register(models.Producto)
class Producto(ImportExportModelAdmin):
    list_display = ('codigo','descripcion',)
    search_fields = ('codigo','descripcion',)

@admin.register(models.Categoria_Gastos)
class Categoria_Gastos(ImportExportModelAdmin):
    list_display = ('descripcion','uc',)
    search_fields = ('descripcion','uc',)

@admin.register(models.Gastos)
class Gastos(ImportExportModelAdmin):
    list_display = ('descripcion','fc',)
    search_fields = ('descripcion','fc',)