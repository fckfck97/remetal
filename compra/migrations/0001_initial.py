# Generated by Django 4.0 on 2022-12-19 03:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.BooleanField(default=True)),
                ('fc', models.DateTimeField(auto_now_add=True)),
                ('fm', models.DateTimeField(auto_now=True)),
                ('um', models.IntegerField(blank=True, null=True)),
                ('razon_social', models.CharField(max_length=100, unique=True)),
                ('tipo', models.CharField(choices=[('Seleccion Una Opcion:', 'Seleccion Una Opcion:'), ('Natural', 'Natural'), ('Jurídico', 'Jurídica'), ('Extranjero', 'Extranjero')], default='Seleccion Una Opcion:', max_length=25)),
                ('rif', models.CharField(max_length=15)),
                ('direccion', models.CharField(blank=True, max_length=250, null=True)),
                ('direccion2', models.CharField(blank=True, max_length=250, null=True)),
                ('telefono', models.CharField(blank=True, max_length=11, null=True)),
                ('email', models.EmailField(blank=True, max_length=255, null=True)),
                ('saldo_favor', models.FloatField(blank=True, default=0, null=True)),
                ('saldo_deudor', models.FloatField(blank=True, default=0, null=True)),
                ('uc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
            options={
                'verbose_name_plural': 'Proveedores',
            },
        ),
        migrations.CreateModel(
            name='ComprasEnc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.BooleanField(default=True)),
                ('fc', models.DateTimeField(auto_now_add=True)),
                ('fm', models.DateTimeField(auto_now=True)),
                ('um', models.IntegerField(blank=True, null=True)),
                ('fecha_compra', models.DateField(blank=True, null=True)),
                ('observacion', models.TextField(blank=True, null=True)),
                ('no_factura', models.CharField(max_length=100)),
                ('fecha_factura', models.DateField()),
                ('sub_total', models.FloatField(default=0)),
                ('total', models.FloatField(default=0)),
                ('pagado', models.BooleanField(default=False)),
                ('monto', models.FloatField(blank=True, default=0, null=True)),
                ('abono_monto', models.FloatField(blank=True, default=0, null=True)),
                ('abono_monto_total', models.FloatField(blank=True, default=0, null=True)),
                ('abono', models.BooleanField(default=False)),
                ('tipo_pago', models.CharField(blank=True, max_length=50, null=True)),
                ('user_cobra', models.CharField(blank=True, max_length=50, null=True)),
                ('descuento', models.FloatField(default=0)),
                ('proveedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='compra.proveedor')),
                ('uc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
            options={
                'verbose_name': 'Encabezado Compra',
                'verbose_name_plural': 'Encabezado Compras',
            },
        ),
        migrations.CreateModel(
            name='ComprasDet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.BooleanField(default=True)),
                ('fc', models.DateTimeField(auto_now_add=True)),
                ('fm', models.DateTimeField(auto_now=True)),
                ('um', models.IntegerField(blank=True, null=True)),
                ('cantidad', models.FloatField(default=0)),
                ('precio_prv', models.FloatField(default=0)),
                ('sub_total', models.FloatField(default=0)),
                ('total', models.FloatField(default=0)),
                ('costo', models.FloatField(default=0)),
                ('descuento', models.FloatField(default=0)),
                ('compra', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='compra.comprasenc')),
            ],
            options={
                'verbose_name': 'Detalle Compra',
                'verbose_name_plural': 'Detalles Compras',
            },
        ),
    ]
