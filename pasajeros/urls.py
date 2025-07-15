from django.urls import path
from . import views

urlpatterns = [
    path('crear/', views.crear_pasajero, name='crear_pasajero'),
]
