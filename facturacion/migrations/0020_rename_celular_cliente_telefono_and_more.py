# Generated by Django 4.0 on 2022-10-06 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facturacion', '0019_remove_cliente_apellidos_remove_cliente_nombres_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cliente',
            old_name='celular',
            new_name='telefono',
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='domicilio',
        ),
        migrations.AddField(
            model_name='cliente',
            name='direccion',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='cliente',
            name='email',
            field=models.EmailField(default='', max_length=255),
            preserve_default=False,
        ),
    ]
