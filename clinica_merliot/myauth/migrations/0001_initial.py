# Generated by Django 2.0.6 on 2018-06-28 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=25, unique=True, verbose_name='Nombre de usuario')),
                ('email', models.EmailField(max_length=100, unique=True, verbose_name='email address')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='profiles/')),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Usuario',
                'verbose_name_plural': 'Usuarios',
                'ordering': ['username'],
            },
        ),
    ]
