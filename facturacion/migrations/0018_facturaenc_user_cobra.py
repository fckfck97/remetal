# Generated by Django 4.1 on 2022-08-20 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facturacion', '0017_alter_facturaenc_tipo_pago'),
    ]

    operations = [
        migrations.AddField(
            model_name='facturaenc',
            name='user_cobra',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]