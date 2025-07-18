from django.db import models
from vuelos.models import Vuelo
from aviones.models import Asiento
from pasajeros.models import Pasajero
from django.core.exceptions import ValidationError
import uuid
from django.utils.timezone import now


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
    activa = models.BooleanField(default=True)

    def clean(self):
        if self.asiento.avion != self.vuelo.avion:
            raise ValidationError("El asiento seleccionado no pertenece al avión asignado a este vuelo.")

    def __str__(self):
        return f"Reserva {self.pk} - {self.pasajero.nombre} para {self.vuelo}"
    
    def generar_boleto(self):
        """Crea un boleto asociado a esta reserva."""
        return Boleto.objects.create(
            reserva=self,
            codigo_barra=str(uuid.uuid4().hex[:20]),
            fecha_emision=now(),
            estado='Emitido'
        )

    class Meta:
        constraints = []

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