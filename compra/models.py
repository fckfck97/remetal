from django.db import models
from base.models import BaseModelo
from inventario.models import Producto
#PARA LOS SIGNAL

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum

class Proveedor(BaseModelo):
    SEL='Seleccion Una Opcion:'
    NAT='Natural'
    JUR='Jurídico'
    EXT='Extranjero'
    TIPO_CLIENTE = [
        (SEL,'Seleccion Una Opcion:'),
        (NAT,'Natural'),
        (JUR,'Jurídica'),
        (EXT,'Extranjero')
    ]
    razon_social=models.CharField(
        max_length=100,
        unique=True
        )
    tipo=models.CharField(
        max_length=25,
        choices=TIPO_CLIENTE,
        default=SEL
    )
    rif=models.CharField(
        max_length=15

    )
    direccion=models.CharField(
        max_length=250,
        null=True, blank=True
        )
    direccion2=models.CharField(
        max_length=250,
        null=True, blank=True
        )
    telefono=models.CharField(
        max_length=11,
        null=True, blank=True
    )
    email=models.EmailField(
        max_length=255,
        null=True, blank=True
    )

    def __str__(self):
        return '{}'.format(self.razon_social)

    def save(self):
        self.razon_social = self.razon_social.upper()

        super(Proveedor, self).save()

    class Meta:
        verbose_name_plural = "Proveedores"

class ComprasEnc(BaseModelo):
    fecha_compra=models.DateField(blank=True,null=True)
    observacion=models.TextField(blank=True,null=True)
    no_factura=models.CharField(max_length=100)
    fecha_factura=models.DateField()
    sub_total=models.FloatField(default=0)
    total=models.FloatField(default=0)
    pagado=models.BooleanField(default=False)
    monto = models.FloatField(default=0,null=True, blank=True)
    tipo_pago=models.CharField(max_length=50,null=True, blank=True)
    user_cobra=models.CharField(max_length=50,null=True,blank=True)
    descuento=models.FloatField(default=0)
    proveedor=models.ForeignKey(Proveedor,on_delete=models.CASCADE)
    
    def __str__(self):
        return '{}'.format(self.observacion)

    
    def save(self):
        self.observacion = self.observacion.upper()
        if self.sub_total == None  or self.descuento == None:
            self.sub_total = 0
            self.descuento = 0
            
        self.total = self.sub_total + self.descuento
        super(ComprasEnc,self).save()

    class Meta:
        verbose_name_plural = "Encabezado Compras"
        verbose_name="Encabezado Compra"

class ComprasDet(BaseModelo):
    compra=models.ForeignKey(ComprasEnc,on_delete=models.CASCADE)
    producto=models.ForeignKey(Producto,on_delete=models.CASCADE)
    cantidad=models.FloatField(default=0)
    precio_prv=models.FloatField(default=0)
    sub_total=models.FloatField(default=0)
    total=models.FloatField(default=0)
    costo=models.FloatField(default=0)
    descuento=models.FloatField(default=0)

    def __str__(self):
        return '{}'.format(self.producto)

    def save(self):
        self.sub_total = float(float(self.cantidad) * float(self.precio_prv))
        self.total = self.sub_total + float(self.descuento)
        super(ComprasDet, self).save()
    
    class Mega:
        verbose_name_plural = "Detalles Compras"
        verbose_name="Detalle Compra"

@receiver(post_delete, sender=ComprasDet)
def detalle_compra_borrar(sender,instance, **kwargs):
    id_producto = instance.producto.id
    id_compra = instance.compra.id

    enc = ComprasEnc.objects.filter(pk=id_compra).first()
    if enc:
        sub_total = ComprasDet.objects.filter(compra=id_compra).aggregate(Sum('sub_total'))
        enc.sub_total=sub_total['sub_total__sum']
        enc.save()
    
    prod=Producto.objects.filter(pk=id_producto).first()
    if prod:
        cantidad = float(prod.existencia) - float(instance.cantidad)
        prod.existencia = cantidad
        prod.save()


@receiver(post_save, sender=ComprasDet)
def detalle_compra_guardar(sender,instance,**kwargs):
    id_producto = instance.producto.id
    fecha_compra=instance.compra.fecha_compra

    prod=Producto.objects.filter(pk=id_producto).first()
    if prod:
        cantidad = float(prod.existencia) + float(instance.cantidad)
        prod.existencia = cantidad
        prod.ultima_compra=fecha_compra
        prod.save()