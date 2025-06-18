from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class RegisterForm(forms.Form):
    username = forms.CharField(
        max_length=50,
        label='Nombre de usuario',
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                'placeholder': 'Ingrese su nombre de usuario'
            }
        )
    )
    password1 = forms.CharField(
        max_length=50,
        label='Contraseña',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control',
                'placeholder': 'Ingrese su contraseña'
            }
        )
    )
    password2 = forms.CharField(
        max_length=50,
        label='Confirmar Contraseña',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control',
                'placeholder': 'Confirme su contraseña'
            }
        )
    )
    email = forms.EmailField(
        max_length=100,
        label='Correo Electrónico',
        widget=forms.EmailInput(
            attrs={'class': 'form-control',
                'placeholder': 'Ingrese su correo electrónico'
            }
        )
    )
    
    def clean(self):
        cleaned_data = super().clean()
        pass1 = cleaned_data.get('password1')
        pass2 = cleaned_data.get('password2')
        if pass1 != pass2:
            raise ValidationError('Las contraseñas no coinciden')
        if User.objects.filter(username=cleaned_data.get('username')).exists():
            raise ValidationError('El nombre de usuario ya está en uso')
        if User.objects.filter(email=cleaned_data.get('email')).exists():
            raise ValidationError('El correo electrónico ya está en uso')
        return cleaned_data