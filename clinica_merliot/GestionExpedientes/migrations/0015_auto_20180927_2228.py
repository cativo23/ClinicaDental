# Generated by Django 2.0.6 on 2018-09-28 04:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GestionExpedientes', '0014_cita_observacioncita'),
    ]

    operations = [
        migrations.AddField(
            model_name='cita',
            name='estado',
            field=models.CharField(choices=[('A', 'Aplicada'), ('F', 'Pendiente'), ('N', 'No Asistio')], default=None, max_length=3),
        ),
        migrations.AlterField(
            model_name='cita',
            name='fechaCita',
            field=models.DateField(help_text='Formato: AAAA-MM-DD', verbose_name='Fecha de Cita'),
        ),
        migrations.AlterField(
            model_name='cita',
            name='horaCita',
            field=models.TimeField(verbose_name='Hora de Cita'),
        ),
    ]
