# Generated by Django 4.1 on 2022-08-15 17:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('compra', '0003_rename_descuento_comprasenc_gastos_adicionales_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comprasdet',
            old_name='descuento',
            new_name='gastos_adicionales',
        ),
    ]
