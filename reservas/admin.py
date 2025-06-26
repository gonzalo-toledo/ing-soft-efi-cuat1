from django.contrib import admin

from .models import Pasajero, Reserva, Boleto

@admin.register(Pasajero)
class PasajeroAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'pasaporte', 'fecha_nacimiento', 'nacionalidad', 'genero', 'email', 'telefono')
    search_fields = ('nombre', 'pasaporte', 'email')
    list_filter = ('nacionalidad', 'genero')    
    
@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('pasajero', 'vuelo', 'asiento', 'fecha_reserva', 'estado')
    search_fields = ('pasajero__nombre', 'vuelo__numero_vuelo', 'asiento__numero')
    list_filter = ('estado', 'vuelo')
    
@admin.register(Boleto)
class BoletoAdmin(admin.ModelAdmin):
    list_display = ('reserva', 'codigo_barra', 'fecha_emision', 'estado')
    search_fields = ('codigo_barra', 'reserva__pasajero__nombre')
    list_filter = ('estado',)