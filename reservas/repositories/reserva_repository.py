from reservas.models import Reserva
from django.shortcuts import get_object_or_404

class ReservaRepository:

    @staticmethod
    def get_all():
        return Reserva.objects.all()
    
    @staticmethod
    def get_flight_reservations(vuelo_id):
        """ Obtiene todas las reservas asociadas a un vuelo específico.
        
        :param flight_id: ID del vuelo.
        :return: QuerySet de reservas asociadas al vuelo.
        """
        return Reserva.objects.filter(vuelo_id=vuelo_id)

    @staticmethod
    def get_by_asiento(asiento_id):
        """ Obtiene una reserva por el ID del asiento.
        
        :param asiento_id: ID del asiento.
        :return: Reserva asociada al asiento o None si no existe.
        """
        return Reserva.objects.filter(asiento_id=asiento_id).first()

    @staticmethod
    def get_by_id(reserva_id):
        return get_object_or_404(Reserva, id=reserva_id)

    @staticmethod
    def get_by_pasajero(pasajero_id):
        return Reserva.objects.filter(pasajero_id=pasajero_id)

    @staticmethod
    def create(**kwargs):
        reserva = Reserva(**kwargs)
        reserva.full_clean()  # valida asiento-vuelo
        reserva.save()
        return reserva

    @staticmethod
    def update(reserva, **kwargs):
        for attr, value in kwargs.items():
            setattr(reserva, attr, value)
        reserva.full_clean()
        reserva.save()
        return reserva

    @staticmethod
    def delete(reserva):
        reserva.delete()
