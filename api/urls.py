from django.urls import path
from .views import ProductoList, ProductoDetalle

urlpatterns = [


    path('productos/',ProductoList.as_view(),name='producto_api'),
    path('productos/<str:codigo>',ProductoDetalle.as_view(),name='producto_api_detalle'),

]