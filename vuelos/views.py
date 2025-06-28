from django.views.generic import ListView, DetailView
from vuelos.models import Vuelo
from aviones.models import Asiento
from reservas.models import Reserva


class VueloList(ListView):
    model = Vuelo
    template_name = 'vuelos/list.html'
    context_object_name = 'vuelos'
    
    def get_queryset(self):
        # Solo mostrar vuelos programados
        return Vuelo.objects.filter(estado='Programado').select_related('avion', 'origen', 'destino')


class VueloDetailView(DetailView):
    model = Vuelo
    template_name = 'vuelos/detail.html'
    context_object_name = 'vuelo'
    pk_url_kwarg = 'vuelo_id'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vuelo = self.get_object()
        
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