from django import forms
from reservas.models import Reserva, Boleto
from pasajeros.models import Pasajero

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['pasajero']  # Solo el pasajero es seleccionable
        
    def __init__(self, *args, **kwargs):
        # Recibir el usuario para filtrar pasajeros
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Solo mostrar pasajeros del usuario actual
        if self.user:
            self.fields['pasajero'].queryset = Pasajero.objects.filter(usuario=self.user)


class BoletoForm(forms.ModelForm):
    class Meta:
        model = Boleto
        fields = ['reserva']