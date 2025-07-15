from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, View
from django.shortcuts import get_object_or_404, redirect, render
from reservas.models import Reserva, Boleto
from reservas.forms import ReservaForm
from vuelos.models import Vuelo
from aviones.models import Asiento
from pasajeros.forms import PasajeroForm

# ==== RESERVAS ====

class ReservaListView(ListView):
    model = Reserva
    template_name = 'reservas/list.html'
    context_object_name = 'reservas'
    
    def get_queryset(self):
        reservas = Reserva.objects.select_related('pasajero__usuario', 'vuelo', 'asiento').order_by('-fecha_reserva')
        # Filtrar reservas por el usuario actual
        if self.request.user.is_authenticated:
            reservas = reservas.filter(pasajero__usuario=self.request.user)
        else:
            messages.error(self.request, "Debe iniciar sesión para ver sus reservas.")
            return Reserva.objects.none()
        return reservas

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
        context['pasajero_form'] = PasajeroForm()
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
        self.object.save()

        messages.success(
            self.request, 
            f"Reserva creada exitosamente para el vuelo {self.vuelo.origen} → "
            f"{self.vuelo.destino} en el asiento {self.asiento.numero}."
        )
        return redirect(self.success_url)
    
    
class ReservaConfirmarPagoView(View):
    def get(self, request, reserva_id):
        reserva = get_object_or_404(Reserva, id=reserva_id)
        return render(request, 'reservas/confirmar_pago.html', {'reserva': reserva})

    def post(self, request, reserva_id):
        reserva = get_object_or_404(Reserva, id=reserva_id)

        if reserva.estado != 'Confirmada':
            reserva.estado = 'Confirmada'
            reserva.save()
            reserva.generar_boleto()
            messages.success(request, "Pago confirmado y boleto generado correctamente.")
        else:
            messages.info(request, "La reserva ya estaba confirmada.")

        return redirect(reverse_lazy('reserva_detail', kwargs={'reserva_id': reserva.id}))

    
class ReservaCancelView(View):
    def get(self, request, *args, **kwargs):
        reserva = get_object_or_404(Reserva, pk=kwargs['reserva_id'])
        return render(request, 'reservas/cancel.html', {'reserva': reserva})

    def post(self, request, *args, **kwargs):
        reserva = get_object_or_404(Reserva, pk=kwargs['reserva_id'])
        reserva.estado = 'Cancelada'
        reserva.save()

        try:
            boleto = Boleto.objects.get(reserva=reserva)
            boleto.estado = 'Anulado'
            boleto.save()
        except Boleto.DoesNotExist:
            pass

        messages.success(request, "Reserva y boleto cancelados correctamente.")
        return redirect(reverse_lazy('reserva_list'))


# ==== BOLETOS ====

class BoletoListView(ListView):
    model = Boleto
    template_name = 'boletos/list.html'
    context_object_name = 'boletos'
    
    def get_queryset(self):
        boletos = Boleto.objects.select_related('reserva__pasajero', 'reserva__vuelo', 'reserva__asiento').order_by('-fecha_emision')
        # Filtrar boletos por el usuario actual
        if self.request.user.is_authenticated:
            boletos = boletos.filter(reserva__pasajero__usuario=self.request.user)
        else:
            messages.error(self.request, "Debe iniciar sesión para ver sus boletos.")
            return Boleto.objects.none()
        return boletos
    
    
class BoletoDetailView(DetailView):
    model = Boleto
    template_name = 'boletos/detail.html'
    context_object_name = 'boleto'
    pk_url_kwarg = 'boleto_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reserva'] = self.object.reserva
        return context