# Generated by Django 4.1 on 2022-08-22 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0003_producto_codigo_barra'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='codigo',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True),
        ),
    ]
