from django.db import models
from vuelos.models import Vuelo
from aviones.models import Asiento
from pasajeros.models import Pasajero
from django.core.exceptions import ValidationError


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

    def clean(self):
        if self.asiento.avion != self.vuelo.avion:
            raise ValidationError("El asiento seleccionado no pertenece al avión asignado a este vuelo.")

    def __str__(self):
        return f"Reserva {self.pk} - {self.pasajero.nombre} para {self.vuelo}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['vuelo', 'asiento'], name='unique_reserva_por_vuelo_y_asiento'),
            models.UniqueConstraint(fields=['pasajero', 'vuelo'], name='unique_reserva_por_pasajero_y_vuelo')
        ]

class Boleto(models.Model):
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE)
    codigo_barra = models.CharField(max_length=20, unique=True)
    fecha_emision = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(
        max_length=20, 
        choices=[
            ('Emitido', 'Emitido'),
            ('Anulado', 'Anulado')
        ], 
        default='Emitido'
    )
    def __str__(self):
        return f"Boleto {self.codigo_barra} - {self.reserva.pasajero.nombre}"
    
    class Meta:
        ordering = ['fecha_emision']