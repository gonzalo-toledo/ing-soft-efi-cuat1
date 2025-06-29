from django.db import models

class Avion(models.Model):
    modelo = models.CharField(max_length=100)
    capacidad = models.IntegerField(blank=True, null=True)  # Capacidad total del avión, se calcula automáticamente
    filas = models.IntegerField()
    columnas = models.IntegerField()

    def save(self, *args, **kwargs):
        es_nuevo = self.pk is None  # Si no tiene PK, es nuevo
        super().save(*args, **kwargs)  # Primero se guarda el avión (necesitamos el ID)
        
        if es_nuevo:
            self.capacidad = self.filas * self.columnas
            letras = [chr(65 + i) for i in range(self.columnas)]  # ['A', 'B', 'C', ...]

            for fila in range(1, self.filas + 1):
                for letra in letras:
                    numero = f"{fila}{letra}"
                    tipo = 'P' if fila <= 2 else 'E'  # Primera clase hasta la fila 2
                    
                    Asiento.objects.create(
                        avion=self,
                        numero=numero,
                        fila=fila,
                        columna=letra,
                        tipo=tipo
                    )

            # Vuelvo a guardar para actualizar la capacidad (opcional, o podés calcular antes)
            super().save(update_fields=['capacidad'])

    def __str__(self):
        return self.modelo


class Asiento(models.Model):
    avion = models.ForeignKey(Avion, on_delete=models.CASCADE)
    numero = models.CharField(max_length=10)
    fila = models.IntegerField()
    columna = models.CharField(max_length=1)
    tipo = models.CharField(max_length=20, choices=[('E', 'Económico'), ('P', 'Primera Clase')])
    
    def __str__(self):
        return f"{self.numero} - {self.tipo}"
