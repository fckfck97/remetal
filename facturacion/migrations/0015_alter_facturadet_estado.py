# Generated by Django 4.1 on 2022-08-19 02:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facturacion', '0014_facturadet_user_borra'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facturadet',
            name='estado',
            field=models.BooleanField(default=False),
        ),
    ]
