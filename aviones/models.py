from django.db import models

# Create your models here.

class Avion(models.Model):
    modelo = models.CharField(max_length=100)
    capacidad = models.IntegerField(blank=True, null=True)  # Capacidad total del avión
    filas = models.IntegerField()
    columnas = models.IntegerField()
    
    def save(self, *args, **kwargs):
        self.capacidad = self.filas * self.columnas
        super().save(*args, **kwargs)
    def __str__(self):
        return self.modelo
    
class Asiento(models.Model):
    avion = models.ForeignKey(Avion, on_delete=models.CASCADE)
    numero = models.CharField(max_length=10)
    fila = models.IntegerField()
    columna = models.CharField(max_length=1)
    tipo = models.CharField(max_length=20, choices=[('E', 'Económico'), ('P', 'Primera Clase')])
    estado = models.CharField(max_length=20, choices=[('Disponible', 'Disponible'), ('Reservado', 'Reservado'), ('Ocupado', 'Ocupado')], default='Disponible')
    
    def __str__(self):
        return f"{self.numero} - {self.tipo} - {self.estado}"