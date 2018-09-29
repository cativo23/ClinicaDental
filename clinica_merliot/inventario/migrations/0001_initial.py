# Generated by Django 2.0.6 on 2018-09-24 17:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_producto', models.CharField(max_length=30, verbose_name='Nombre del producto')),
                ('marca_producto', models.CharField(max_length=30, verbose_name='Marca del producto')),
                ('existencia_producto', models.IntegerField(verbose_name='Exitencias')),
                ('precio_producto', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Precio')),
            ],
        ),
        migrations.CreateModel(
            name='Registro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_registro', models.CharField(choices=[('compra', 'Compra'), ('venta', 'Venta'), ('caduco', 'Caduco')], max_length=10, verbose_name='Tipo de registro')),
                ('cantidad_registro', models.IntegerField(verbose_name='Cantidad')),
                ('fecha_registro', models.DateField(help_text='Formato: AAAA-MM-DD', verbose_name='Fecha de registro')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventario.Producto')),
            ],
        ),
    ]