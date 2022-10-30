from django.urls import path
from .views import CategoriaView, CategoriaNew, CategoriaEdit, inhabilitarcat,\
    SubCategoriaNew, SubCategoriaView, SubCategoriaNew, SubCategoriaEdit, inhabilitarsubcat, \
    ProductoView, ProductoNew, ProductoEdit, inhabilitarproducto,\
    GastosView, GastosNew, GastosEdit, inhabilitargasto,\
    Categoria_Gastos_View, Categoria_Gastos_Edit, Categoria_Gastos_New, inhabilitarcatgas
from .reporte import imprimir_todo_producto, imprimir_gastos


urlpatterns = [
    # vistas listas urls
    path('categorias/', CategoriaView.as_view(), name="lista_categoria"),
    path('categoria/nueva', CategoriaNew.as_view(), name='nueva_categoria'),
    path('categoria/editar/<pk>', CategoriaEdit.as_view(), name='editar_categoria'),
    path('categoria/estado/<int:id>', inhabilitarcat,
         name='inhabilitar_categoria'),


    path('subcategorias/', SubCategoriaView.as_view(), name="lista_subcategoria"),
    path('subcategorias/nueva', SubCategoriaNew.as_view(),
         name='nueva_subcategoria'),
    path('subcategoria/editar/<pk>', SubCategoriaEdit.as_view(),
         name='editar_subcategoria'),
    path('subcategoria/estado/<int:id>', inhabilitarsubcat,
         name='inhabilitar_subcategoria'),



    path('producto/', ProductoView.as_view(), name="lista_productos"),
    path('producto/nuevo', ProductoNew.as_view(), name='nuevos_productos'),
    path('producto/editar/<pk>', ProductoEdit.as_view(), name='editar_productos'),
    path('producto/estado/<int:id>', inhabilitarproducto,
         name='inhabilitar_producto'),
    path('producto/imprimir-todas/<str:f1>/<str:f2>',
         imprimir_todo_producto, name="imprimir_producto"),


    path('gastos/', GastosView.as_view(), name="lista_gastos"),
    path('gastos/nueva', GastosNew.as_view(),
         name='nuevo_gastos'),
    path('gastos/editar/<pk>', GastosEdit.as_view(),
         name='editar_gastos'),
    path('gastos/estado/<int:id>', inhabilitargasto,
         name='inhabilitar_gastos'),
     path('gastos/imprimir-todas/<str:f1>/<str:f2>',
         imprimir_gastos, name="imprimir_gastos"),

    path('categorias/gastos/', Categoria_Gastos_View.as_view(),
         name="lista_categoria_gastos"),
    path('categoria/gastos/nueva', Categoria_Gastos_New.as_view(),
         name='nueva_categoria_gastos'),
    path('categoria/gastos/editar/<pk>', Categoria_Gastos_Edit.as_view(),
         name='editar_categoria_gastos'),
    path('categoria/gastos/estado/<int:id>', inhabilitarcatgas,
         name='inhabilitar_categoria_gastos'),

]
