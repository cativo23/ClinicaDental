# Generated by Django 2.0.6 on 2018-11-27 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GestionExpedientes', '0002_auto_20181125_2320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cita',
            name='fechaCita',
            field=models.DateTimeField(verbose_name='date_created'),
        ),
    ]
