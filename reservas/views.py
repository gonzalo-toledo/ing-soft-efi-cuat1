from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView
from django.shortcuts import get_object_or_404, redirect
from reservas.models import Reserva, Boleto
from reservas.forms import ReservaForm
from vuelos.models import Vuelo
from aviones.models import Asiento
from pasajeros.models import Pasajero

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
        # Asegurarnos de que el usuario está autenticado
        kwargs['user'] = self.request.user
        
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
        # Obtener los datos del formulario
        pasajero = form.cleaned_data['pasajero']

        # Verificar si el pasajero ya tiene una reserva para este vuelo
        reserva_existente = Reserva.objects.filter(
            vuelo=self.vuelo,
            pasajero=pasajero,
            estado__in=['Confirmada', 'Pendiente']
        ).exists()

        if reserva_existente:
            messages.error(
                self.request, 
                f"El pasajero {pasajero} ya tiene una reserva para este vuelo."
            )
            return redirect('vuelo_detail', vuelo_id=self.vuelo.id)        
        self.object = form.save(commit=False)
        self.object.estado = 'Confirmada'
        self.object.save()

        # Crear boleto automáticamente
        self.object.generar_boleto()

        messages.success(
            self.request, 
            f"Reserva y boleto creados exitosamente para el vuelo {self.vuelo.origen} → "
            f"{self.vuelo.destino} en el asiento {self.asiento.numero}."
        )
        return redirect(self.success_url)
    
class ReservaCancelView(DeleteView):
    model = Reserva
    template_name = 'reservas/cancel.html'
    pk_url_kwarg = 'reserva_id'
    success_url = reverse_lazy('reserva_list')

    def delete(self, request, *args, **kwargs):
        reserva = self.get_object()
        reserva.estado = 'Cancelada'
        reserva.save()

        # Anular boleto si existe
        try:
            boleto = Boleto.objects.get(reserva=reserva)
            boleto.estado = 'Anulado'
            boleto.save()
        except Boleto.DoesNotExist:
            pass

        messages.success(request, "Reserva y boleto cancelados correctamente.")
        return redirect(self.success_url)

# ==== BOLETOS ====

class BoletoListView(ListView):
    model = Boleto
    template_name = 'boletos/list.html'
    context_object_name = 'boletos'
    
    def get_queryset(self):
        return Boleto.objects.select_related('reserva__pasajero', 'reserva__vuelo', 'reserva__asiento').order_by('-fecha_emision')
    
class BoletoDetailView(DetailView):
    model = Boleto
    template_name = 'boletos/detail.html'
    context_object_name = 'boleto'
    pk_url_kwarg = 'boleto_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reserva'] = self.object.reserva
        return context