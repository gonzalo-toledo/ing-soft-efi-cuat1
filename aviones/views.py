from django.shortcuts import render
from aviones.services.avion_service import AvionService
#! from aviones.services.asiento_service import AsientoService
from django.shortcuts import get_object_or_404
from aviones.models import Avion

# Create your views here.

def aviones_list(request):
    all_aviones = AvionService.get_all()
    return render(request,
                'aviones/aviones_list.html',
                {
                    'aviones': all_aviones
                })
    
def aviones_detail(request, avion_id):
    avion =  get_object_or_404(Avion, id = avion_id)
    return render(request,
                'aviones/aviones_detail.html',
                {
                    'avion': avion
                })
    
