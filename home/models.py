from django.db import models

class Nacionalidad(models.Model):
    codigo = models.CharField(max_length=2, unique=True)
    pais = models.CharField(max_length=100)
    gentilicio = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.pais} ({self.codigo})"
