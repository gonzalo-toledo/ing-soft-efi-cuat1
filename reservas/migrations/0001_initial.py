# Generated by Django 5.2.3 on 2025-06-25 22:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pasajero',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('pasaporte', models.CharField(max_length=20, unique=True)),
                ('fecha_nacimiento', models.DateField()),
                ('nacionalidad', models.CharField(max_length=50)),
                ('genero', models.CharField(choices=[('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')], max_length=10)),
                ('email', models.EmailField(max_length=254)),
                ('telefono', models.CharField(max_length=15)),
            ],
        ),
    ]
