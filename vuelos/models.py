from django.db import models
from aviones.models import (
    Avion,
)

    
class Aeropuerto(models.Model):
    iata = models.CharField(max_length=3, unique=True)
    nombre = models.CharField(max_length=255)
    ciudad = models.CharField(max_length=100)
    provincia = models.CharField(max_length=100)
    pais = models.CharField(max_length=100)
    latitud = models.FloatField()
    longitud = models.FloatField()
    tipo = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.iata} - {self.nombre}"
    
class Vuelo(models.Model):
    avion = models.ForeignKey(Avion, on_delete=models.CASCADE)
    origen = models.ForeignKey(Aeropuerto, on_delete=models.CASCADE, related_name='vuelos_origen')
    destino = models.ForeignKey(Aeropuerto, on_delete=models.CASCADE, related_name='vuelos_destino')
    fecha_salida = models.DateTimeField()
    fecha_llegada = models.DateTimeField()
    duracion = models.DurationField(blank=True, null=True)  # Duración del vuelo
    estado = models.CharField(max_length=20, choices=[
        ('Programado', 'Programado'),
        ('En Vuelo', 'En Vuelo'),
        ('Aterrizado', 'Aterrizado'),
        ('Cancelado', 'Cancelado'),
        ('Retrasado', 'Retrasado')
    ], default='Programado')
    precio_base = models.DecimalField(max_digits=10, decimal_places=2)
    
    def save(self, *args, **kwargs):
        if self.fecha_salida and self.fecha_llegada:
            self.duracion = self.fecha_llegada - self.fecha_salida
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Vuelo de {self.origen} a {self.destino}, Avión: {self.avion.modelo} ({self.fecha_salida.strftime('%Y-%m-%d %H:%M')})"
    