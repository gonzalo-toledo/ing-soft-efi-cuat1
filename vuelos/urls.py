from django.urls import path

from vuelos.views import VueloList, VueloDetailView

urlpatterns = [
    path('', 
         VueloList.as_view(), 
         name='vuelo_list'),
    path('<int:vuelo_id>/', 
         VueloDetailView.as_view(), 
         name='vuelo_detail'),
]