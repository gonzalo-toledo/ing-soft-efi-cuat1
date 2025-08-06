from aviones.models import Asiento
from pasajeros.forms import PasajeroForm
from vuelos.models import Vuelo
from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, View
from reservas.forms import ReservaForm
from django.http import HttpResponse
from weasyprint import HTML
from django.templatetags.static import static
from reservas.models import Boleto, Reserva

import tempfile
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
            activa=True,
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
            activa=True,
            estado__in=['Confirmada', 'Pendiente']
        ).exists()


        if reserva_existente:
            messages.error(
                self.request, 
                f"El pasajero {pasajero} ya tiene una reserva para este vuelo."
            )
            return redirect('vuelo_detail', vuelo_id=self.vuelo.id)        
        self.object = form.save(commit=False)
        self.object.activa = True
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

        if reserva.estado != 'Confirmada' and reserva.estado != 'Cancelada':
            reserva.estado = 'Confirmada'
            reserva.save()
            reserva.generar_boleto()

            try:
                boleto = Boleto.objects.get(reserva=reserva)
            except Boleto.DoesNotExist:
                messages.error(request, "No se pudo encontrar el boleto generado.")
                return redirect(reverse_lazy('reserva_detail', kwargs={'reserva_id': reserva.id}))

            # Obtenemos los datos directamente del pasajero
            username = reserva.pasajero.nombre
            email_destino = reserva.pasajero.email

            if not email_destino or not username:
                messages.error(request, "Faltan datos del usuario para enviar el email.")
                return redirect(reverse_lazy('reserva_detail', kwargs={'reserva_id': reserva.id}))

            # Renderizamos el contenido HTML del email
            message = render_to_string(
                'emails/boleto.html',
                {
                    'username': username,
                    'email': email_destino,
                    'boleto': boleto,
                }
            )

            # Creamos y enviamos el email
            email = EmailMessage(
                subject='Skyway - Confirmación de Pago y Boleto Emitido',
                body=message,
                from_email=settings.EMAIL_HOST_USER,
                to=[email_destino]
            )
            email.content_subtype = 'html'

            try:
                email.send(fail_silently=False)
                messages.success(request, "Pago confirmado, boleto generado y email enviado.")
            except Exception as e:
                messages.warning(request, f"El boleto fue generado, pero ocurrió un error al enviar el mail: {e}")

        elif reserva.estado == 'Cancelada':
            messages.error(request, "La reserva ya estaba cancelada.")
        else:
            messages.info(request, "La reserva ya estaba confirmada.")

        return redirect(reverse_lazy('reserva_detail', kwargs={'reserva_id': reserva.id}))

    
class ReservaCancelView(View):
    def get(self, request, *args, **kwargs):
        reserva = get_object_or_404(Reserva, pk=kwargs['reserva_id'])
        return render(request, 'reservas/cancel.html', {'reserva': reserva})

    def post(self, request, *args, **kwargs):
        reserva = get_object_or_404(Reserva, pk=kwargs['reserva_id'])
        if reserva.estado in ['Pendiente', 'Confirmada']:
            reserva.estado = 'Cancelada'
            reserva.activa = False
            reserva.save()
        
            try:
                boleto = Boleto.objects.get(reserva=reserva)
                boleto.estado = 'Anulado'
                boleto.save()
            except Boleto.DoesNotExist:
                pass

            messages.success(request, "Reserva y boleto cancelados correctamente.")
            return redirect(reverse_lazy('reserva_list'))
        else:
            messages.error(request, "La reserva ya estaba cancelada y no se puede modificar.")
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
    


class BoletoPDFView(View):
    def get(self, request, boleto_id):
        boleto = get_object_or_404(Boleto, pk=boleto_id)

        # Construir la URL absoluta de la imagen de fondo
        bg_relative_url = static('img/bg-boleto.png')  # Usa tu ruta real dentro de /static/
        bg_url = request.build_absolute_uri(bg_relative_url)

        # Renderizar el HTML con la URL de fondo incluida
        html_string = render_to_string('boletos/pdf_template.html', {
            'boleto': boleto,
            'bg_url': bg_url
        })

        # Crear PDF con WeasyPrint
        with tempfile.NamedTemporaryFile(delete=True, suffix='.pdf') as temp_pdf:
            HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(target=temp_pdf.name)
            temp_pdf.seek(0)
            pdf_data = temp_pdf.read()

        # Devolver el PDF como respuesta HTTP
        response = HttpResponse(pdf_data, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename=boleto_{boleto.id}.pdf'
        return response
