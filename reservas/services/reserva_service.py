from reservas.repositories.reserva_repository import ReservaRepository

class ReservaService:
    
    

    @staticmethod
    def crear_reserva(data):
        return ReservaRepository.create(**data)

    @staticmethod
    def cancelar_reserva(reserva_id):
        reserva = ReservaRepository.get_by_id(reserva_id)
        reserva.estado = 'Cancelada'
        return ReservaRepository.update(reserva, estado='Cancelada')
