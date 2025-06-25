from django.urls import path

from vuelos.views import VueloList

urlpatterns = [
    path(route='vuelo_list/', 
        view=VueloList.as_view(), 
        name='vuelo_list',
    ),
]