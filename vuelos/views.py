from django.views.generic import ListView, DetailView
from vuelos.models import Vuelo
from aviones.models import Asiento
from reservas.models import Reserva
from django.db.models.functions import TruncDate
from django.contrib import messages
from django.shortcuts import redirect
from datetime import date
from django.contrib.auth.mixins import UserPassesTestMixin

class VueloList(ListView):
    model = Vuelo
    template_name = 'vuelos/list.html'
    context_object_name = 'vuelos'
    
    def get_queryset(self):
        # Paso 1: Traer todos los vuelos que podrían necesitar actualización
        todos_los_vuelos = Vuelo.objects.filter(
            estado__in=['Programado', 'En Vuelo', 'Aterrizado']
        ).select_related('avion', 'origen', 'destino')

        # Paso 2: Actualizar el estado de cada vuelo
        for vuelo in todos_los_vuelos:
            vuelo.actualizar_estado()

        # Paso 3: Filtrar en memoria los que ahora están Programado o En Vuelo
        vuelos_mostrables = [
            vuelo for vuelo in todos_los_vuelos
            if vuelo.estado in ['Programado', 'En Vuelo']
        ]

        return vuelos_mostrables
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Agregar información adicional para los filtros
        # vuelos = self.get_queryset()
        
        # Obtener origenes y destinos únicos para los filtros
        # origenes_unicos = vuelos.values_list('origen__iata', 'origen__ciudad').distinct().order_by('origen__ciudad')
        # destinos_unicos = vuelos.values_list('destino__iata', 'destino__ciudad').distinct().order_by('destino__ciudad')
        
        # context['origenes_unicos'] = origenes_unicos
        # context['destinos_unicos'] = destinos_unicos
        
        return context


class VueloDetailView(DetailView):
    model = Vuelo
    template_name = 'vuelos/detail.html'
    context_object_name = 'vuelo'
    pk_url_kwarg = 'vuelo_id'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vuelo = self.get_object()
        vuelo.actualizar_estado() # Actualizar el estado del vuelo
        
        # Obtener todos los asientos del avión
        asientos_avion = Asiento.objects.filter(avion=vuelo.avion).order_by('numero')
        
        # Obtener asientos ya reservados para este vuelo
        asientos_reservados = Reserva.objects.filter(
            vuelo=vuelo, 
            estado__in=['Confirmada', 'Pendiente']
        ).values_list('asiento_id', flat=True)
        
        # Marcar asientos como disponibles/ocupados
        asientos_disponibles = []
        asientos_ocupados = []
        
        for asiento in asientos_avion:
            if asiento.id in asientos_reservados:
                asientos_ocupados.append(asiento)
            else:
                asientos_disponibles.append(asiento)
        
        context['asientos_disponibles'] = asientos_disponibles
        context['asientos_ocupados'] = asientos_ocupados
        context['total_asientos'] = len(asientos_avion)
        context['asientos_libres'] = len(asientos_disponibles)
        
        return context
    
    
class BuscarVueloView(ListView):
    model = Vuelo
    template_name = 'vuelos/list.html'  # Usar el mismo template
    context_object_name = 'vuelos'

    def get(self, request, *args, **kwargs):
        origen = request.GET.get('origen')
        destino = request.GET.get('destino')
        fecha = request.GET.get('fecha')

        # Validación: origen y destino no pueden ser iguales
        if origen and destino and origen == destino:
            messages.error(request, "El origen y el destino no pueden ser iguales.")
            return redirect('vuelo_list')

        # Validación: fecha no puede ser anterior a hoy
        if fecha and fecha < date.today().isoformat():
            messages.error(request, "La fecha no puede ser anterior a hoy.")
            return redirect('vuelo_list')

        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        origen = self.request.GET.get('origen')
        destino = self.request.GET.get('destino')
        fecha = self.request.GET.get('fecha')

        queryset = Vuelo.objects.filter(
            estado__in=['Programado', 'En Vuelo', 'Aterrizado']
        )

        if origen:
            queryset = queryset.filter(origen__iata=origen)
        if destino:
            queryset = queryset.filter(destino__iata=destino)
        if fecha:
            queryset = queryset.annotate(
                fecha_solo=TruncDate('fecha_salida')
            ).filter(fecha_solo=fecha)

        vuelos = queryset.select_related('avion', 'origen', 'destino')
        
        for vuelo in vuelos:
            vuelo.actualizar_estado()  # 🔄 También acá actualizás el estado

        return vuelos

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtener todos los vuelos para los filtros (sin filtrar)
        todos_vuelos = Vuelo.objects.filter(estado='Programado').select_related('avion', 'origen', 'destino')
        
        # Obtener origenes y destinos únicos para los filtros
        origenes_unicos = todos_vuelos.values_list('origen__iata', 'origen__ciudad').distinct().order_by('origen__ciudad')
        destinos_unicos = todos_vuelos.values_list('destino__iata', 'destino__ciudad').distinct().order_by('destino__ciudad')
        
        context['origenes_unicos'] = origenes_unicos
        context['destinos_unicos'] = destinos_unicos
        
        # Agregar información de filtros activos
        # context['filtros_activos'] = {
        #     'origen': self.request.GET.get('origen'),
        #     'destino': self.request.GET.get('destino'),
        #     'fecha': self.request.GET.get('fecha'),
        # }
        
        return context

# Mixin y vistas para staff

class StaffRequiredMixin(UserPassesTestMixin):
    """Mixin para verificar que el usuario sea staff"""
    def test_func(self):
        return self.request.user.is_staff
    

class VuelosPasajerosStaffView(StaffRequiredMixin, ListView):
    """Vista para mostrar todos los vuelos con sus pasajeros - Solo para staff"""
    model = Vuelo
    template_name = 'staff/staff_pasajeros.html'
    context_object_name = 'vuelos'
    
    def get_queryset(self):
        vuelos = Vuelo.objects.filter(
            estado__in=['Programado', 'En Vuelo', 'Aterrizado', 'Cancelado', 'Retrasado']
        ).select_related('avion', 'origen', 'destino').prefetch_related(
            'reserva_set__pasajero',
            'reserva_set__asiento'
        ).order_by('-fecha_salida')
        for vuelo in vuelos:
            vuelo.actualizar_estado()  # 🔄 También acá actualizás el estado

        return vuelos
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtener información de pasajeros para cada vuelo
        vuelos_con_pasajeros = []
        for vuelo in context['vuelos']:
            reservas = vuelo.reserva_set.filter(
                estado__in=['Confirmada', 'Pendiente']
            ).select_related('pasajero__usuario', 'asiento')
            
            pasajeros = []
            for reserva in reservas:
                pasajeros.append({
                    'pasajero': reserva.pasajero,
                    'asiento': reserva.asiento,
                    'estado_reserva': reserva.estado,
                    'fecha_reserva': reserva.fecha_reserva if hasattr(reserva, 'fecha_reserva') else None
                })
            
            vuelos_con_pasajeros.append({
                'vuelo': vuelo,
                'pasajeros': pasajeros,
                'total_pasajeros': len(pasajeros)
            })
        
        context['vuelos'] = vuelos_con_pasajeros
        return context


class VueloPasajerosDetailStaffView(StaffRequiredMixin, DetailView):
    """Vista detallada de un vuelo específico con sus pasajeros - Solo para staff"""
    model = Vuelo
    template_name = 'staff/staff_vuelo_detail.html'
    context_object_name = 'vuelo'
    pk_url_kwarg = 'vuelo_id'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vuelo = self.get_object()
        
        # Obtener todas las reservas del vuelo
        reservas = Reserva.objects.filter(vuelo=vuelo).select_related(
            'pasajero', 'asiento'
        ).order_by('asiento__numero')
        
        # Separar por estado
        reservas_confirmadas = reservas.filter(estado='Confirmada')
        reservas_pendientes = reservas.filter(estado='Pendiente')
        reservas_canceladas = reservas.filter(estado='Cancelada')
        
        context.update({
            'reservas_confirmadas': reservas_confirmadas,
            'reservas_pendientes': reservas_pendientes,
            'reservas_canceladas': reservas_canceladas,
            'total_reservas': reservas.count(),
            'total_confirmadas': reservas_confirmadas.count(),
            'total_pendientes': reservas_pendientes.count(),
            'total_canceladas': reservas_canceladas.count(),
        })
        
        return context