import json
from django.core.management.base import BaseCommand
from home.models import Nacionalidad

class Command(BaseCommand):
    help = "Carga nacionalidades desde un archivo JSON"

    def handle(self, *args, **kwargs):
        with open("home/management/jsons/nacionalidades.json", encoding="utf-8") as f:
            data = json.load(f)

        for item in data:
            Nacionalidad.objects.update_or_create(
                codigo=item["codigo"],
                defaults={
                    "pais": item["pais"],
                    "gentilicio": item["gentilicio"]
                }
            )
        self.stdout.write(self.style.SUCCESS("✔ Nacionalidades cargadas correctamente."))
