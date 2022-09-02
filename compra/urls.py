from django.urls import path, include

from .views import ProveedorView, ProveedorNew, ProveedorEdit, inhabilitarpro,\
    ComprasView, compras, CompraDetDelete, CompraEncDelete, pago_compra
from .reportes import imprimir_factura_compra,imprimir_factura_compra_todas


urlpatterns = [

    path('proveedores/',ProveedorView.as_view(), name="lista_proveedores"),
    path('proveedores/nuevo/',ProveedorNew.as_view(), name="nuevo_proveedor"),
    path('proveedores/editar/<pk>',ProveedorEdit.as_view(), name="editar_proveedor"),
    path('proveedores/estado/<int:id>',inhabilitarpro, name="inhabilitar_proveedor"),
    

    path('vista/',ComprasView.as_view(), name="lista_compras"),
    path('nueva/',compras, name="nueva_compra"),
    path('edit/<int:compra_id>',compras, name="editar_compra"),
    path('<int:compra_id>/delete/<int:pk>',CompraDetDelete.as_view(), name="eliminar_compra"),
    path('eliminar/<int:pk>',CompraEncDelete.as_view(), name="eliminar_enc"),

    path('compras/listado', imprimir_factura_compra_todas, name='imprimir_factura_compra_todas'),
    path('compras/<int:id>/imprimir', imprimir_factura_compra,name="imprimir_factura_compra"),
    path('pago_compra/<int:id>',pago_compra, name="pago_compra"),
    
]