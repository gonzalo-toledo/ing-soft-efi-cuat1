from django.db import models
from django.contrib.auth.models import User
from home.models import Nacionalidad

class Pasajero(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    pasaporte = models.CharField(max_length=20)
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
        return f'{self.nombre}, {self.apellido} '
    