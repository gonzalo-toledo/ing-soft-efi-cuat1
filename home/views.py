from django.shortcuts import render, redirect
from django.views import View
from home.forms import LoginForm, RegisterForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from pasajeros.models import Pasajero
from reservas.models import Reserva
from pasajeros.forms import PasajeroForm

# Create your views here.

class PerfilView(View):
    def get(self, request):
        pasajeros = Pasajero.objects.filter(usuario=request.user)      
        reservas = Reserva.objects.filter(pasajero__in=pasajeros).select_related('vuelo', 'pasajero', 'asiento')
        reservas_vuelos_aterrizados = reservas.filter(vuelo__estado='Aterrizado').order_by('-vuelo__fecha_salida')
        form = PasajeroForm()
        return render(
            request, 
            'account/perfil.html',
            {
                'pasajeros': pasajeros,
                'reservas_vuelos_aterrizados': reservas_vuelos_aterrizados,
                'form': form,
            }
        )

class HomeView(View):
    def get(self, request):
        return render(
            request, 
            'index.html'
        )

class RegisterView(View):
    def get(self, request):
        return redirect(request.META.get('HTTP_REFERER', 'index'))
    
    def post(self, request):
        form = RegisterForm(request.POST)
        next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or 'index'
        if form.is_valid():
            User.objects.create_user(    
                username = form.cleaned_data.get('username'),
                password = form.cleaned_data.get('password1'),
                email = form.cleaned_data.get('email'),
            )
            messages.success(request, 'Usuario registrado correctamente')
            return redirect(next_url)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(
                        request,
                        f"{form.fields[field].label}: {error}" if field in form.fields else error
                    )
            return redirect(next_url)
class LoginView(View):
    def get(self, request):
        return redirect('index')
        # Para permitir renderización directa del login:
        # return render(request, 'account/login.html', {'form': LoginForm()})

    def post(self, request):
        form = LoginForm(request.POST)
        next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or 'index'

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(next_url)
            else:
                messages.error(request, "Usuario o contraseña incorrectos")
        else:
            messages.error(request, "Formulario inválido")

        # Redirigimos a la página anterior (o index si no hay otra)
        return redirect(next_url)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('index')