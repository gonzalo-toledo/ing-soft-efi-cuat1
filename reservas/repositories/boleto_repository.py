from reservas.models import Boleto
from django.shortcuts import get_object_or_404

class BoletoRepository:

    @staticmethod
    def get_all():
        return Boleto.objects.all()

    @staticmethod
    def get_by_id(boleto_id):
        return get_object_or_404(Boleto, id=boleto_id)

    @staticmethod
    def get_by_codigo_barra(codigo):
        return Boleto.objects.filter(codigo_barra=codigo).first()

    @staticmethod
    def create(**kwargs):
        return Boleto.objects.create(**kwargs)

    @staticmethod
    def delete(boleto):
        boleto.delete()
