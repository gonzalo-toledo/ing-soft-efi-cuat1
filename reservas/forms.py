from django import forms
from reservas.models import Reserva
from pasajeros.models import Pasajero

class ReservaForm(forms.ModelForm):
    """
    Formulario para crear reservas.
    Solo permite seleccionar el pasajero, el vuelo y asiento se pasan por URL.
    """
    class Meta:
        model = Reserva
        fields = ['pasajero']  # Solo el pasajero es seleccionable por el usuario
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            # Mostrar pasajeros que pertenecen al usuario actual
            self.fields['pasajero'].queryset = Pasajero.objects.filter(usuario=user)
            
            # Mejorar la apariencia del campo
            self.fields['pasajero'].widget.attrs.update({
                'class': 'form-control',
                'required': True
            })
            
            # Texto de ayuda si no hay pasajeros
            if not self.fields['pasajero'].queryset.exists():
                self.fields['pasajero'].help_text = (
                    "No tienes pasajeros registrados. "
                    "Debes crear un pasajero antes de hacer una reserva."
                )
        else:
            # Si no hay usuario, no mostrar pasajeros
            self.fields['pasajero'].queryset = Pasajero.objects.none()
