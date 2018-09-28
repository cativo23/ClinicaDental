# Generated by Django 2.0.6 on 2018-09-28 03:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('GestionExpedientes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Consulta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechaConsulta', models.DateField(auto_now_add=True, verbose_name='Fecha de Consulta')),
                ('horaInicio', models.TimeField(auto_now_add=True, verbose_name='Hora de inicio')),
                ('horaFinal', models.TimeField(null=True, verbose_name='Hora de Final')),
                ('observacionCons', models.TextField(blank=True, max_length=250, null=True, verbose_name='Observaciones')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='GestionExpedientes.Doctor')),
            ],
            options={
                'verbose_name': 'Consulta',
                'verbose_name_plural': 'Consultas',
                'ordering': ['fechaConsulta', 'horaInicio'],
            },
        ),
        migrations.CreateModel(
            name='Odontograma',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechaCreacion', models.DateTimeField(auto_now_add=True, verbose_name='date_created')),
                ('notas', models.TextField()),
                ('medico', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='GestionExpedientes.Doctor')),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GestionExpedientes.Paciente')),
            ],
        ),
        migrations.CreateModel(
            name='Procedimiento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pieza', models.IntegerField()),
                ('cara', models.CharField(choices=[('S', 'Vestibular'), ('C', 'Oclusal'), ('X', 'Pieza Completa'), ('Z', 'Distal'), ('D', 'Mesial'), ('I', 'Palatino')], max_length=4)),
                ('diagnostico', models.TextField()),
                ('notas', models.TextField(blank=True)),
                ('status', models.CharField(choices=[('recomendado', 'Recomendado'), ('autorizado', 'Autorizado'), ('en_proceso', 'En Proceso'), ('completado', 'Completado')], default='recomendado', max_length=12)),
                ('odontograma', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='odontograma.Odontograma')),
            ],
        ),
        migrations.CreateModel(
            name='Tratamiento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombreTratamiento', models.CharField(max_length=100, verbose_name='Nombre del tratamiento')),
                ('descripcionTratamiento', models.TextField(blank=True, max_length=250, null=True, verbose_name='Descripcion del tratamiento')),
                ('precioBase', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Precio Base')),
            ],
            options={
                'verbose_name': 'Tratamiento',
                'verbose_name_plural': 'Tratamientos',
                'ordering': ['nombreTratamiento'],
            },
        ),
        migrations.AddField(
            model_name='procedimiento',
            name='tratamiento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='odontograma.Tratamiento'),
        ),
        migrations.AddField(
            model_name='consulta',
            name='odontograma',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='odontograma.Odontograma'),
        ),
        migrations.AddField(
            model_name='consulta',
            name='paciente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='GestionExpedientes.Expediente'),
        ),
    ]
