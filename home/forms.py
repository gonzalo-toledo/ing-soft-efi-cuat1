from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class RegisterForm(forms.Form):
    username = forms.CharField(
        max_length=50,
        label='Nombre de usuario',
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                'placeholder': 'Nombre de usuario'
            }
        )
    )
    password1 = forms.CharField(
        max_length=50,
        label='Contraseña',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control',
                'placeholder': 'Contraseña'
            }
        )
    )
    password2 = forms.CharField(
        max_length=50,
        label='Confirmar Contraseña',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control',
                'placeholder': 'Confirmar contraseña'
            }
        )
    )
    email = forms.EmailField(
        max_length=100,
        label='Correo Electrónico',
        widget=forms.EmailInput(
            attrs={'class': 'form-control',
                'placeholder': 'Correo electrónico'
            }
        )
    )
    
    def clean_username(self):
        username = self.cleaned_data.get('username').lower()
        if User.objects.filter(username=username).exists():
            raise ValidationError('El nombre de usuario ya está en uso')       
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        if User.objects.filter(email=email).exists():
            raise ValidationError('El correo electrónico ya está en uso')
        return email
    
    #!VALIDACION DE CONTRASEÑA - DESCOMENTAR ANTES DE ENTREGAR EL PROYECTO
    # def clean_password1(self):
    #     password1 = self.cleaned_data.get('password1')
    #     if len(password1) < 8:
    #         raise ValidationError('La contraseña debe tener al menos 8 caracteres')
    #     if not re.search(r'[A-Z]', password1):
    #         raise ValidationError('La contraseña debe contener al menos una letra mayúscula')
    #     if not re.search(r'[a-z]', password1):
    #         raise ValidationError('La contraseña debe contener al menos una letra minúscula')
    #     if not re.search(r'[0-9]', password1):
    #         raise ValidationError('La contraseña debe contener al menos un número')  
    #     return password1
    
    def clean(self):
        cleaned_data = super().clean()
        pass1 = cleaned_data.get('password1')
        pass2 = cleaned_data.get('password2')
        if pass1 != pass2:
            raise ValidationError('Las contraseñas no coinciden')
        return cleaned_data
    
    
class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=50,
        label='Nombre de usuario',
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                'placeholder': 'Nombre de usuario'
            }
        )
    )

    password = forms.CharField(
        max_length=50,
        label='Contraseña',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control',
                'placeholder': 'Contraseña'
            }
        )
    )
    
    def clean_username(self):
        return self.cleaned_data['username'].lower()