# Generated by Django 2.0.6 on 2018-09-25 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myauth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='sex',
            field=models.CharField(choices=[('M', 'Masculino'), ('F', 'Femenino')], default=None, max_length=2),
        ),
    ]