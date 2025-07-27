from django import forms 
from .models import Pasajero
from django.utils import timezone




class PasajeroForm(forms.ModelForm):
    class Meta:
        model = Pasajero
        exclude = ['usuario']
        labels = {
            'fecha_nacimiento': 'Fecha de Nacimiento',
            'nombre': 'Nombre',
            'apellido': 'Apellido',
            'pasaporte': 'Documento de Identidad',
            'nacionalidad': 'Nacionalidad',
            'genero': 'Género',
            'email': 'Correo Electrónico',
            'telefono': 'Teléfono',
        }
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'pasaporte': forms.TextInput(attrs={'class': 'form-control'}),
            'nacionalidad': forms.Select(attrs={'class': 'form-control'}),
            'genero': forms.Select(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
        }
