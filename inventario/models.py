from django.db import models
from base.models import BaseModelo
# Create your models here.

class Categoria(BaseModelo):
    descripcion = models.CharField(
        max_length=100,
        help_text='Descripción de la Categoría',
        unique=True
    )

    def __str__(self):
        return '{}'.format(self.descripcion)

    def save(self):
        self.descripcion = self.descripcion.upper()
        super(Categoria, self).save()

    class Meta:
        verbose_name_plural= "Categorias"

class SubCategoria(BaseModelo):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    descripcion = models.CharField(
        max_length=100,
        help_text='Descripción de la Categoría'
    )

    def __str__(self):
        return '{}:{}'.format(self.categoria.descripcion,self.descripcion)
    
    def save(self):
        self.descripcion = self.descripcion.upper()
        super(SubCategoria, self).save()

    class Meta:
        verbose_name_plural= "Sub Categorias"
        unique_together = ('categoria','descripcion')

class Producto(BaseModelo):
    codigo = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
        null=True

    )
    descripcion = models.CharField(max_length=200)
    precio = models.FloatField(default=0)
    existencia = models.IntegerField(default=0)
    ultima_compra = models.DateField(null=True, blank=True)

    subcategoria = models.ForeignKey(SubCategoria, on_delete=models.CASCADE)
    foto = models.ImageField(upload_to="images/",null=True,blank=True)

    def __str__(self):
        return '{}'.format(self.descripcion)
    
    def save(self):
        self.descripcion = self.descripcion.upper()
        super(Producto,self).save()
   

    
    class Meta:
        verbose_name_plural = "Productos"
        unique_together = ('codigo', 'descripcion')



class Categoria_Gastos(BaseModelo):
    descripcion = models.CharField(
        max_length=100,
        help_text='Descripción de la Categoría',
        unique=True
    )

    def __str__(self):
        return '{}'.format(self.descripcion)

    def save(self):
        self.descripcion = self.descripcion.upper()
        super(Categoria_Gastos, self).save()

    class Meta:
        verbose_name_plural= "Categorias de Gastos"


class Gastos(models.Model):
    descripcion = models.CharField(max_length=250,blank=True,null=True)
    monto_gastos = models.FloatField(default=0)
    estado = models.BooleanField(default=True)
    fc = models.DateTimeField(auto_now_add=True)
    fm = models.DateTimeField(auto_now=True)
    categoria = models.ForeignKey(Categoria_Gastos, on_delete=models.CASCADE)
    def __str__(self):
        return '{}'.format(self.descripcion)

    class Mega:
        verbose_name_plural = "Gastos de Compras"
        verbose_name="Gastos de Compra"
