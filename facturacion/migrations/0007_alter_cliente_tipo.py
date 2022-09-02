# Generated by Django 4.1 on 2022-08-13 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facturacion', '0006_alter_cliente_tipo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='tipo',
            field=models.CharField(choices=[('Seleccion Una Opcion:', 'Seleccion Una Opcion:'), ('Natural', 'Natural'), ('Jurídico', 'Jurídica'), ('Extranjero', 'Extranjero')], default='Seleccion Una Opcion:', max_length=25),
        ),
    ]