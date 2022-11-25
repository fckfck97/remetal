from django.urls import path, include

from .views import  PerfilView,ProveedorView,ProveedorNew, ProveedorEdit,\
    ComprasView, compras, CompraDetDelete, CompraEncDelete, pago_compra
from .reportes import imprimir_factura_compra,imprimir_factura_list,imprimir_general_proveedor


urlpatterns = [
    path('proveedores/',ProveedorView.as_view(), name="lista_proveedor"),
    path('proveedores/perfil/<int:id>',PerfilView.as_view(), name="perfil_proveedor"),
    path('proveedores/nuevo',ProveedorNew.as_view(), name="nuevo_proveedor"),
    path('proveedores/edit/<pk>',ProveedorEdit.as_view(), name="editar_proveedor"),
    path('proveedores/general/<int:id>/imprimir', imprimir_general_proveedor,name="imprimir_general_proveedor"),

    path('factura/',ComprasView.as_view(), name="lista_compras"),
    path('factura/new/',compras, name="nueva_compra"),
    path('factura/edit/<int:compra_id>',compras, name="editar_compra"),
    path('factura/<int:compra_id>/delete/<int:pk>',CompraDetDelete.as_view(), name="eliminar_compra"),
    path('factura/eliminar/<int:pk>',CompraEncDelete.as_view(), name="eliminar_enc"),

    path('factura/imprimir-todas/<str:f1>/<str:f2>',imprimir_factura_list, name="factura_imprimir_all"),
    path('factura/compras/<int:id>/imprimir', imprimir_factura_compra,name="imprimir_factura_compra"),
    path('factura/pago_compra/<int:id>',pago_compra, name="pago_compra"),
    
]