from django.contrib import admin
from aviones.models import Avion, Asiento

# Register your models here.
@admin.register(Avion)
class AvionAdmin(admin.ModelAdmin):
    list_display = ('modelo', 'capacidad', 'filas', 'columnas')
    search_fields = ('modelo',)
    list_filter = ('capacidad',)
    ordering = ('modelo',)
    list_per_page = 20
    exclude = ('capacidad',)

@admin.register(Asiento)
class AsientoAdmin(admin.ModelAdmin):
    list_display = ('numero', 'fila', 'columna', 'tipo')
    search_fields = ('numero', 'tipo')
    list_filter = ('tipo',)
    list_per_page = 20
