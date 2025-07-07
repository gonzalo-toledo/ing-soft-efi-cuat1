# urls.py (en tu app de vuelos)
from django.urls import path
from . import views

urlpatterns = [
    # Lista de vuelos (página principal)
    path('', views.VueloList.as_view(), name='vuelo_list'),
    
    # Búsqueda de vuelos con filtros
    path('buscar/', views.BuscarVueloView.as_view(), name='buscar_vuelos'),
    
    # Detalle de vuelo
    path('<int:vuelo_id>/', views.VueloDetailView.as_view(), name='vuelo_detail'),
    
    # URLs para staff
    path('staff/pasajeros/', views.VuelosPasajerosStaffView.as_view(), name='vuelos_pasajeros_staff'),
    path('staff/vuelo/<int:vuelo_id>/pasajeros/', views.VueloPasajerosDetailStaffView.as_view(), name='vuelo_pasajeros_detail_staff'),
]