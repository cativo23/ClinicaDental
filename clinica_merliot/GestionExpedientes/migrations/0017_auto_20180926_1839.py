# Generated by Django 2.0.6 on 2018-09-27 00:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GestionExpedientes', '0016_merge_20180926_1531'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paciente',
            name='fechaNacimiento',
            field=models.DateField(help_text='Formato: DD-MM-AAAA', verbose_name='Fecha de nacimiento'),
        ),
    ]
