from django.contrib import admin

# Register your models here.
from vuelos.models import (
    Vuelo, 
    Aeropuerto,
)
@admin.register(Vuelo)
class VueloAdmin(admin.ModelAdmin):
    list_display = ('avion', 'origen', 'destino', 'fecha_salida', 'fecha_llegada', 'duracion', 'estado', 'precio_base')
    search_fields = ('origen', 'destino', 'avion__modelo')
    list_filter = ('estado', 'fecha_salida')
    date_hierarchy = 'fecha_salida'
    ordering = ('-fecha_salida',)
    list_per_page = 20
    exclude = ('duracion',)
    
    
@admin.register(Aeropuerto)
class AeropuertoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'ciudad', 'provincia', 'pais', 'iata', 'tipo')
    search_fields = ('nombre', 'ciudad', 'provincia', 'pais', 'iata')
    list_filter = ('pais', 'tipo')
    ordering = ('nombre',)
    list_per_page = 20
    exclude = ('latitud', 'longitud')
    readonly_fields = ('latitud', 'longitud')