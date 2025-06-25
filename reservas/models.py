from django.db import models
from home.models import Nacionalidad
from vuelos.models import Vuelo
from aviones.models import Asiento

class Pasajero(models.Model):
    nombre = models.CharField(max_length=100)
    pasaporte = models.CharField(max_length=20, unique=True)
    fecha_nacimiento = models.DateField()
    nacionalidad = models.ForeignKey(Nacionalidad, on_delete=models.CASCADE)
    genero = models.CharField(
    max_length=10, 
        choices=[
            ('M', 'Masculino'),
            ('F', 'Femenino'),
            ('O', 'Otro'),
            ]
    )
    email = models.EmailField()
    telefono = models.CharField(max_length=15)

    def __str__(self):
        return self.nombre
    

class Reserva(models.Model):
    pasajero = models.ForeignKey(Pasajero, on_delete=models.CASCADE)
    vuelo = models.ForeignKey(Vuelo, on_delete=models.CASCADE)
    asiento = models.ForeignKey(Asiento, on_delete=models.CASCADE)
    fecha_reserva = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(
        max_length=20, 
        choices=[
            ('Confirmada', 'Confirmada'),
            ('Pendiente', 'Pendiente'),
            ('Cancelada', 'Cancelada')
        ], 
        default='Pendiente'
    )

    def __str__(self):
        return f"Reserva {self.pk} - {self.pasajero.nombre} para {self.vuelo}"
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['vuelo', 'asiento'], name='unique_reserva_por_vuelo_y_asiento')
        ]