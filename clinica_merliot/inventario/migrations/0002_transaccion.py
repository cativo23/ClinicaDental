# Generated by Django 2.0.6 on 2018-11-06 14:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaccion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_transaccion', models.CharField(choices=[('ENTRADA', 'ENTRADA'), ('SALIDA', 'SALIDA')], max_length=7, verbose_name='Tipo de registro')),
                ('fecha', models.DateField(help_text='Formato: AAAA-MM-DD', verbose_name='Fecha de registro')),
                ('cantidad', models.IntegerField(verbose_name='Cantidad')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventario.Producto')),
            ],
        ),
    ]
