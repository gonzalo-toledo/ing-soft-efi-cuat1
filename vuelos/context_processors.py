from vuelos.models import Aeropuerto

def aeropuertos_disponibles(request):
    """
    processor que devuelve una lista de aeropuertos ordenados por ciudad.
    """
    aeropuertos = Aeropuerto.objects.all()
    return {'aeropuertos': aeropuertos}