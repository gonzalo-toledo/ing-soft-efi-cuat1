from django.contrib import admin

# Register your models here.
from vuelos.models import Vuelo

@admin.register(Vuelo)
class VueloAdmin(admin.ModelAdmin):
    list_display = ('avion', 'origen', 'destino', 'fecha_salida', 'fecha_llegada', 'duracion', 'estado', 'precio_base')
    search_fields = ('origen', 'destino', 'avion__modelo')
    list_filter = ('estado', 'fecha_salida')
    date_hierarchy = 'fecha_salida'
    ordering = ('-fecha_salida',)
    list_per_page = 20
    exclude = ('duracion',)