# Generated by Django 4.1 on 2022-08-15 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compra', '0002_remove_proveedor_contacto_alter_proveedor_email'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comprasenc',
            old_name='descuento',
            new_name='gastos_adicionales',
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='email',
            field=models.EmailField(max_length=255),
        ),
    ]