# Generated by Django 5.2.3 on 2025-06-25 22:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aviones', '0002_alter_avion_capacidad'),
        ('home', '0001_initial'),
        ('reservas', '0001_initial'),
        ('vuelos', '0004_alter_vuelo_destino_alter_vuelo_origen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pasajero',
            name='nacionalidad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.nacionalidad'),
        ),
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_reserva', models.DateTimeField(auto_now_add=True)),
                ('estado', models.CharField(choices=[('Confirmada', 'Confirmada'), ('Pendiente', 'Pendiente'), ('Cancelada', 'Cancelada')], default='Pendiente', max_length=20)),
                ('asiento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aviones.asiento')),
                ('pasajero', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reservas.pasajero')),
                ('vuelo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vuelos.vuelo')),
            ],
            options={
                'constraints': [models.UniqueConstraint(fields=('vuelo', 'asiento'), name='unique_reserva_por_vuelo_y_asiento')],
            },
        ),
    ]
