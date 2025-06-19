from django.shortcuts import render, redirect
from django.views import View
from home.forms import RegisterForm
from django.contrib.auth.models import User
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
            