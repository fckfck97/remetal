from django.db import models
from base.models import BaseModelo, BaseModelo2
from inventario.models import Producto

#Para los signals
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum

class Cliente(BaseModelo):
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

    def save(self, *args, **kwargs):
        self.razon_social = self.razon_social.upper()
        
        super(Cliente, self).save( *args, **kwargs)

    class Meta:
        verbose_name_plural = "Clientes"


class FacturaEnc(BaseModelo2):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha = models.DateTimeField()
    sub_total=models.FloatField(default=0)
    descuento=models.FloatField(default=0)
    total=models.FloatField(default=0)
    pagado=models.BooleanField(default=False)
    monto = models.FloatField(default=0,null=True, blank=True)
    guia=models.CharField(max_length=150,null=True, blank=True)
    numventa=models.CharField(max_length=150,null=True, blank=True)
    tipo_pago=models.CharField(max_length=50,null=True, blank=True)
    user_cobra=models.CharField(max_length=50,null=True,blank=True)

    def __str__(self):
        return '{}'.format(self.id)

    def save(self):
        self.total = self.sub_total - self.descuento
        super(FacturaEnc,self).save()

    class Meta:
        verbose_name_plural = "Encabezado Facturas"
        verbose_name="Encabezado Factura"
        permissions = [
            ('sup_caja_facturaenc','Permisos de Supervisor de Caja Encabezado')
        ]
    

class FacturaDet(BaseModelo2):
    factura = models.ForeignKey(FacturaEnc,on_delete=models.CASCADE)
    producto=models.ForeignKey(Producto,on_delete=models.CASCADE)
    cantidad=models.FloatField(default=0)
    precio=models.FloatField(default=0)
    sub_total=models.FloatField(default=0)
    descuento=models.FloatField(default=0)
    total=models.FloatField(default=0)
    estado=models.BooleanField(default=False)
    user_borra=models.CharField(max_length=50,null=True,blank=True)

    def __str__(self):
        return '{}'.format(self.producto)

    def save(self):
        self.sub_total = float(float((self.cantidad)) * float(self.precio))
        self.total = self.sub_total - float(self.descuento)
        super(FacturaDet, self).save()
    
    class Meta:
        verbose_name_plural = "Detalles Facturas"
        verbose_name="Detalle Factura"
        permissions = [
            ('sup_caja_facturadet','Permisos de Supervisor de Caja Detalle')
        ]



@receiver(post_save, sender=FacturaDet)
def detalle_fac_guardar(sender,instance,**kwargs):
    factura_id = instance.factura.id
    producto_id = instance.producto.id

    enc = FacturaEnc.objects.get(pk=factura_id)
    if enc:
        sub_total = FacturaDet.objects \
            .filter(factura=factura_id) \
            .aggregate(sub_total=Sum('sub_total')) \
            .get('sub_total',0.00)
        
        descuento = FacturaDet.objects \
            .filter(factura=factura_id) \
            .aggregate(descuento=Sum('descuento')) \
            .get('descuento',0.00)
    
        enc.sub_total = sub_total
        enc.descuento = descuento
        enc.save()

    prod=Producto.objects.filter(pk=producto_id).first()
    if prod:
        cantidad = float(prod.existencia) - float(instance.cantidad)
        prod.existencia = cantidad
        prod.save()
