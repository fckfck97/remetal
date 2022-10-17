from django.urls import path
from .views import ClienteView, ClienteNew, ClienteEdit, clienteInactivar,\
    FacturaView, facturas, ProductoView, borrar_detalle_factura, FacturaEncDelete, pago_factura
from .reportes import imprimir_factura_recibo

urlpatterns = [
    
    path('clientes/',ClienteView.as_view(), name="lista_clientes"),
    path('clientes/new',ClienteNew.as_view(), name="nuevo_cliente"),
    path('clientes/<int:pk>',ClienteEdit.as_view(), name="editar_cliente"),
    path('clientes/estado/<int:id>',clienteInactivar, name="inactivar_cliente"),

    path('factura/',FacturaView.as_view(), name="lista_factura"),
    path('factura/new',facturas, name="nueva_factura"),
    path('factura/edit/<int:id>',facturas, name="editar_factura"),
    path('eliminar/<int:pk>',FacturaEncDelete.as_view(), name="eliminar_enc"),
    path('factura/borrar-detalle/<int:id>',borrar_detalle_factura, name="factura_borrar_detalle"),
    path('factura/pago_factura/<int:id>',pago_factura, name="pago_factura"),

    
    path('factura/buscar-producto',ProductoView.as_view(), name="factura_producto"),

    path('factura/imprimir/<int:id>',imprimir_factura_recibo, name="factura_imprimir_one"),





]
