# Generated by Django 5.2.3 on 2025-06-25 22:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Nacionalidad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=2, unique=True)),
                ('pais', models.CharField(max_length=100)),
                ('gentilicio', models.CharField(max_length=100)),
            ],
        ),
    ]
