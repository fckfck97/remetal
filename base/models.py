from django.db import models
from django.contrib.auth.models import User
from django_userforeignkey.models.fields import UserForeignKey

# Create your models here.


class BaseModelo(models.Model):
    estado = models.BooleanField(default=True)
    fc = models.DateTimeField(auto_now_add=True)
    fm = models.DateTimeField(auto_now=True)
    uc = models.ForeignKey(User, on_delete=models.CASCADE)
    um = models.IntegerField(blank=True,null=True)

    class Meta:
        abstract=True


class BaseModelo2(models.Model):
    estado = models.BooleanField(default=True)
    fc = models.DateTimeField(auto_now_add=True)
    fm = models.DateTimeField(auto_now=True)
    # uc = models.ForeignKey(User, on_delete=models.CASCADE)
    # um = models.IntegerField(blank=True,null=True)
    uc = UserForeignKey(auto_user_add=True,related_name='+')
    um = UserForeignKey(auto_user=True,related_name='+')

    class Meta:
        abstract=True




class Gastos(models.Model):
    descripcion = models.CharField(max_length=250,blank=True,null=True)
    monto_gastos = models.FloatField(default=0)
    estado = models.BooleanField(default=True)
    fc = models.DateTimeField(auto_now_add=True)
    fm = models.DateTimeField(auto_now=True)
    def __str__(self):
        return '{}'.format(self.descripcion)

    class Mega:
        verbose_name_plural = "Gastos de Compras"
        verbose_name="Gastos de Compra"