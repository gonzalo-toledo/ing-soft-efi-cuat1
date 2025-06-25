import json
from django.core.management.base import BaseCommand
from vuelos.models import Aeropuerto

class Command(BaseCommand):
    help = "Carga los aeropuertos desde un archivo JSON"

    def handle(self, *args, **kwargs):
        with open("vuelos/management/jsons/aeropuertos.json", encoding="utf-8") as f:
            datos = json.load(f)

        for item in datos:
            Aeropuerto.objects.update_or_create(
                iata=item["iata"],
                defaults={
                    "nombre": item["nombre"],
                    "ciudad": item["ciudad"],
                    "provincia": item["provincia"],
                    "pais": item["pais"],
                    "latitud": item["latitud"],
                    "longitud": item["longitud"],
                    "tipo": item["tipo"]
                }
            )
        self.stdout.write(self.style.SUCCESS("✔ Aeropuertos cargados correctamente."))