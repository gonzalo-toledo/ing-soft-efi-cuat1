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
    """
    Vista para crear una nueva reserva.
    Recibe vuelo_id y asiento_id por URL y valida la disponibilidad.
    """
    model = Reserva
    form_class = ReservaForm
    template_name = 'reservas/create.html'
    success_url = reverse_lazy('reserva_list')

    def dispatch(self, request, *args, **kwargs):
        """
        Método que se ejecuta antes de cualquier procesamiento.
        Aquí validamos que el vuelo y asiento sean válidos y estén disponibles.
        """
        # Obtener IDs de la URL
        vuelo_id = kwargs.get('vuelo_id')
        asiento_id = kwargs.get('asiento_id')
        
        # Validar que ambos IDs existen
        if not vuelo_id or not asiento_id:
            messages.error(request, "Debe seleccionar un vuelo y asiento válidos.")
            return redirect('vuelo_list')
        
        # Obtener objetos desde la base de datos
        self.vuelo = get_object_or_404(Vuelo, id=vuelo_id)
        self.asiento = get_object_or_404(Asiento, id=asiento_id)
        
        # Validar que el asiento pertenece al avión del vuelo
        if self.asiento.avion != self.vuelo.avion:
            messages.error(request, "El asiento no pertenece al avión de este vuelo.")
            return redirect('vuelo_detail', vuelo_id=vuelo_id)
        
        # Validar que el asiento no esté ocupado
        reserva_existente = Reserva.objects.filter(
            vuelo=self.vuelo, 
            asiento=self.asiento,
            estado__in=['Confirmada', 'Pendiente']
        ).exists()
        
        if reserva_existente:
            messages.error(request, "Este asiento ya está reservado.")
            return redirect('vuelo_detail', vuelo_id=vuelo_id)
        
        # Si todo está bien, continuar con el procesamiento normal
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Agregar datos adicionales al contexto del template.
        Enviamos la información del vuelo y asiento seleccionados.
        """
        context = super().get_context_data(**kwargs)
        context['vuelo'] = self.vuelo
        context['asiento'] = self.asiento
        return context

    def get_form_kwargs(self):
        """
        Personalizar los argumentos que se pasan al formulario.
        Aquí pre-asignamos el vuelo y asiento, y pasamos el usuario actual.
        """
        kwargs = super().get_form_kwargs()
        
        # Pasar el usuario actual al formulario para filtrar pasajeros
        kwargs['user'] = self.request.user
        
        # Crear nueva instancia de Reserva con vuelo y asiento pre-asignados
        # Esto evita que el usuario pueda modificar estos valores
        kwargs['instance'] = Reserva(
            vuelo=self.vuelo, 
            asiento=self.asiento
        )
        
        return kwargs

    def form_valid(self, form):
        """
        Método que se ejecuta cuando el formulario es válido.
        Aquí confirmamos la reserva y mostramos mensaje de éxito.
        """
        # El estado por defecto es 'Pendiente' según el modelo
        messages.success(
            self.request, 
            f"Reserva creada exitosamente para el vuelo {self.vuelo.origen} → "
            f"{self.vuelo.destino} en el asiento {self.asiento.numero}."
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