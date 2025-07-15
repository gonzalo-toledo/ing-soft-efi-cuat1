from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import PasajeroForm

@login_required
def crear_pasajero(request):
    if request.method == 'POST':
        form = PasajeroForm(request.POST)
        next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or 'index'
        if form.is_valid():
            pasajero = form.save(commit=False)
            pasajero.usuario = request.user
            pasajero.save()
            return redirect(next_url)
        form = PasajeroForm()
    
    return render(request, 'pasajeros/pasajero_create.html', {'pasajero_form': form})