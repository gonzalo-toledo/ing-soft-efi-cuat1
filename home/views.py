from django.shortcuts import render, redirect
from django.views import View
from home.forms import LoginForm, RegisterForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# Create your views here.

class HomeView(View):
    def get(self, request):
        return render(
            request, 
            'index.html'
        )

class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(
            request,
            'account/register.html',
            {'form': form}
        )
    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            User.objects.create_user(    
                username = form.cleaned_data.get('username'),
                password = form.cleaned_data.get('password1'),
                email = form.cleaned_data.get('email'),
            )
            messages.success(request, 'Usuario registrado correctamente')
            return redirect('index')
        else:
            # Este bloque toma los errores del formulario y los agrega al sistema de mensajes
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{form.fields[field].label}: {error}" if field in form.fields else error)

            return render(request, 'account/register.html', {'form': form})
            
# class LoginView(View):
#     def get(self, request):
#         form = LoginForm()
#         return render(
#             request,
#             'account/login.html',
#             {'form': form}
#         )
    
#     def post(self, request):
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
            
#             user = authenticate ( 
#                 request,
#                 username = username,
#                 password = password
#             )
#             if user is not None:
#                 login(request, user)
#                 return redirect('index')
#             else:
#                 messages.error(request, 'Usuario o contrase')
#                 return redirect('login')
#         else:
#             # Este bloque toma los errores del formulario y los agrega al sistema de mensajes
#             for field, errors in form.errors.items():
#                 for error in errors:
#                     messages.error(request, f"{form.fields[field].label}: {error}" if field in form.fields else error)

#             return render(request, 'account/login.html', {'form': form})
        

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