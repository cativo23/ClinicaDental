# Generated by Django 2.0.6 on 2018-09-27 20:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('GestionExpedientes', '0012_auto_20180628_2304'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cita',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asuntoCita', models.TextField(max_length=50, verbose_name='Asunto de la cita')),
                ('fechaCita', models.DateField(auto_now_add=True, verbose_name='Fecha de Cita')),
                ('horaCita', models.TimeField(auto_now_add=True, verbose_name='Hora de Cita')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='GestionExpedientes.Doctor')),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='GestionExpedientes.Expediente')),
            ],
            options={
                'verbose_name': 'Cita',
                'verbose_name_plural': 'Citas',
                'ordering': ['fechaCita', 'horaCita'],
            },
        ),
        migrations.AlterField(
            model_name='paciente',
            name='fechaNacimiento',
            field=models.DateField(help_text='Formato: AAAA-MM-DD', verbose_name='Fecha de nacimiento'),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='nombresPaciente',
            field=models.CharField(max_length=60, verbose_name='Nombres del paciente'),
        ),
    ]
