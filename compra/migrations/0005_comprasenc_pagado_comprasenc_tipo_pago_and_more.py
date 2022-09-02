# Generated by Django 4.1 on 2022-08-20 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compra', '0004_rename_descuento_comprasdet_gastos_adicionales'),
    ]

    operations = [
        migrations.AddField(
            model_name='comprasenc',
            name='pagado',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='comprasenc',
            name='tipo_pago',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='comprasenc',
            name='user_cobra',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]