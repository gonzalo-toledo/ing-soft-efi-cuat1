from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .forms import PasajeroForm
from django.contrib import messages
from pasajeros.models import Pasajero


@login_required
def crear_pasajero(request):
    if request.method == 'POST':
        form = PasajeroForm(request.POST)
        next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or 'index'
        
        if form.is_valid():
            pasaporte = form.cleaned_data['pasaporte']
            if Pasajero.objects.filter(usuario=request.user, pasaporte=pasaporte).exists():
                messages.error(request, 'Ya tienes un pasajero con este documento de identidad')
                return redirect(next_url)
            
            pasajero = form.save(commit=False)
            pasajero.usuario = request.user
            pasajero.save()
            messages.success(request, 'Pasajero creado correctamente')    
            return redirect(next_url)
        else:
            # Agregar errores detallados del formulario
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(
                        request,
                        f"{form.fields[field].label}: {error}" if field in form.fields else error
                    )
            return redirect(next_url)

    return redirect(request.META.get('HTTP_REFERER', 'index'))
