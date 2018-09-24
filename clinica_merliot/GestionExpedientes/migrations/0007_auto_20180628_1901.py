# Generated by Django 2.0.6 on 2018-06-29 01:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GestionExpedientes', '0006_auto_20180628_1551'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consulta',
            name='fechaConsulta',
            field=models.DateField(auto_now_add=True, verbose_name='Fecha de Consulta'),
        ),
        migrations.AlterField(
            model_name='consulta',
            name='horaInicio',
            field=models.TimeField(auto_now_add=True, verbose_name='Hora de inicio'),
        ),
    ]