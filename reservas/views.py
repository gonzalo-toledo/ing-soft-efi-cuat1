from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView
from django.shortcuts import get_object_or_404, redirect
from reservas.models import Reserva, Boleto
from reservas.forms import ReservaForm, BoletoForm
from vuelos.models import Vuelo
from aviones.models import Asiento

# ==== RESERVAS ====

class ReservaListView(ListView):
    model = Reserva
    template_name = 'reservas/list.html'
    context_object_name = 'reservas'
    
    def get_queryset(self):
        return Reserva.objects.select_related('pasajero', 'vuelo', 'asiento').order_by('-fecha_reserva')


class ReservaDetailView(DetailView):
    model = Reserva
    template_name = 'reservas/detail.html'
    context_object_name = 'reserva'
    pk_url_kwarg = 'reserva_id'


class ReservaCreateView(CreateView):
    model = Reserva
    form_class = ReservaForm
    template_name = 'reservas/create.html'
    success_url = reverse_lazy('reserva_list')

    def dispatch(self, request, *args, **kwargs):
        # Obtener vuelo y asiento de la URL
        self.vuelo_id = kwargs.get('vuelo_id')
        self.asiento_id = kwargs.get('asiento_id')
        
        # Validar que existen
        if not self.vuelo_id or not self.asiento_id:
            messages.error(request, "Debe seleccionar un vuelo y asiento válidos.")
            return redirect('vuelo_list')
        
        # Obtener objetos
        self.vuelo = get_object_or_404(Vuelo, id=self.vuelo_id)
        self.asiento = get_object_or_404(Asiento, id=self.asiento_id)
        
        # Validar que el asiento pertenece al avión del vuelo
        if self.asiento.avion != self.vuelo.avion:
            messages.error(request, "El asiento no pertenece al avión de este vuelo.")
            return redirect('vuelo_detail', vuelo_id=self.vuelo_id)
        
        # Validar que el asiento está disponible
        if self._asiento_ocupado():
            messages.error(request, "Este asiento ya está reservado.")
            return redirect('vuelo_detail', vuelo_id=self.vuelo_id)
        
        return super().dispatch(request, *args, **kwargs)

    def _asiento_ocupado(self):
        """Verifica si el asiento ya está ocupado"""
        return Reserva.objects.filter(
            vuelo=self.vuelo, 
            asiento=self.asiento,
            estado__in=['Confirmada', 'Pendiente']
        ).exists()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vuelo'] = self.vuelo
        context['asiento'] = self.asiento
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Pasar usuario al formulario
        
        # Ensure 'instance' is not None before attempting to set its attributes
        # Create a new Reserva instance if one isn't provided or if it's None
        if kwargs.get('instance') is None:
            kwargs['instance'] = Reserva(vuelo=self.vuelo, asiento=self.asiento)
        else:
            # If an instance already exists, update its vuelo and asiento
            kwargs['instance'].vuelo = self.vuelo
            kwargs['instance'].asiento = self.asiento
        return kwargs

    # Remove form_valid's assignment of vuelo and asiento, as it's now handled in get_form_kwargs
    def form_valid(self, form):
        # form.instance.vuelo and form.instance.asiento are already set by get_form_kwargs
        messages.success(
            self.request, 
            f"Reserva creada para el vuelo {self.vuelo} en el asiento {self.asiento.numero}."
        )
        return super().form_valid(form)


class ReservaCancelView(DeleteView):
    model = Reserva
    template_name = 'reservas/cancel.html'
    pk_url_kwarg = 'reserva_id'
    success_url = reverse_lazy('reserva_list')

    def delete(self, request, *args, **kwargs):
        reserva = self.get_object()
        reserva.estado = 'Cancelada' 
        reserva.save()
        messages.success(request, "Reserva cancelada correctamente.")
        return redirect(self.success_url)


# ==== BOLETOS ====

class BoletoListView(ListView):
    model = Boleto
    template_name = 'boletos/list.html'
    context_object_name = 'boletos'
    
    def get_queryset(self):
        return Boleto.objects.select_related('reserva__pasajero', 'reserva__vuelo').order_by('-fecha_emision')


class BoletoDetailView(DetailView):
    model = Boleto
    template_name = 'boletos/detail.html'
    context_object_name = 'boleto'
    pk_url_kwarg = 'boleto_id'


class BoletoCreateView(CreateView):
    model = Boleto
    form_class = BoletoForm
    template_name = 'boletos/create.html'
    success_url = reverse_lazy('boleto_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Solo reservas confirmadas sin boleto
        reservas_disponibles = Reserva.objects.filter(
            estado='Confirmada'
        ).exclude(
            id__in=Boleto.objects.values_list('reserva_id', flat=True)
        )
        form.fields['reserva'].queryset = reservas_disponibles
        return form

    def form_valid(self, form):
        # Verificar que no existe ya un boleto
        if Boleto.objects.filter(reserva=form.instance.reserva).exists():
            messages.error(self.request, "Esta reserva ya tiene un boleto emitido.")
            return self.form_invalid(form)
        
        # Generar código único
        import uuid
        form.instance.codigo_barra = str(uuid.uuid4()).replace('-', '')[:12].upper()
        
        messages.success(self.request, "Boleto emitido correctamente.")
        return super().form_valid(form)


class BoletoAnularView(DeleteView):
    model = Boleto
    template_name = 'boletos/anular.html'
    pk_url_kwarg = 'boleto_id'
    success_url = reverse_lazy('boleto_list')

    def delete(self, request, *args, **kwargs):
        boleto = self.get_object()
        boleto.estado = 'Anulado'
        boleto.save()
        messages.success(request, "Boleto anulado correctamente.")
        return redirect(self.success_url)