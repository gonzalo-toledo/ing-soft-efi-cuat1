# Generated by Django 5.0.2 on 2025-06-26 20:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aviones', '0002_alter_avion_capacidad'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='asiento',
            name='estado',
        ),
    ]
