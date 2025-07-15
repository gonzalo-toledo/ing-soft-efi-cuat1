from django import forms
from .models import Pasajero

class PasajeroForm(forms.ModelForm):
    class Meta:
        model = Pasajero
        exclude = ['usuario']
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
