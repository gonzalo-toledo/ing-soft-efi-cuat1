
from django.views.generic import ListView
from vuelos.models import Vuelo


# Create your views here.
class VueloList(ListView):
    model = Vuelo
    template_name = 'vuelos/list.html'
    context_object_name = 'vuelos'
    