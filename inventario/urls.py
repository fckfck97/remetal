from django.urls import path
from .views import CategoriaView, CategoriaNew, CategoriaEdit, inhabilitarcat,\
    SubCategoriaNew,SubCategoriaView, SubCategoriaNew, SubCategoriaEdit, inhabilitarsubcat, \
        ProductoView, ProductoNew, ProductoEdit, inhabilitarproducto




urlpatterns = [
    #vistas listas urls
    path('categorias/',CategoriaView.as_view(),name="lista_categoria"),
    path('categoria/nueva',CategoriaNew.as_view(),name='nueva_categoria'),
    path('categoria/editar/<pk>',CategoriaEdit.as_view(),name='editar_categoria'),
    path('categoria/estado/<int:id>',inhabilitarcat,name='inhabilitar_categoria'),


    path('subcategorias/',SubCategoriaView.as_view(),name="lista_subcategoria"),
    path('subcategorias/nueva',SubCategoriaNew.as_view(), name='nueva_subcategoria'),
    path('subcategoria/editar/<pk>',SubCategoriaEdit.as_view(),name='editar_subcategoria'),
    path('subcategoria/estado/<int:id>',inhabilitarsubcat,name='inhabilitar_subcategoria'),



    path('productos/',ProductoView.as_view(),name="lista_productos"),
    path('producto/nuevo',ProductoNew.as_view(), name='nuevos_productos'),
    path('producto/editar/<pk>',ProductoEdit.as_view(),name='editar_productos'),
    path('producto/estado/<int:id>',inhabilitarproducto,name='inhabilitar_producto'),



]   
