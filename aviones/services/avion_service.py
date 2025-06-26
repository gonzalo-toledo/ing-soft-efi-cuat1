from aviones.models import Avion
from aviones.repositories.avion_repository import AvionRepository

class AvionService:
    @staticmethod
    def get_all() -> list[Avion]:
        """
        Obtener todos los aviones.
        """
        return AvionRepository.get_all()

    @staticmethod
    def get_by_id(avion_id: int) -> Avion:
        """
        Obtener un avión por su ID.
        """
        return AvionRepository.get_by_id(avion_id)
    
    @staticmethod
    def create(
        modelo: str,
        filas: int,
        columnas: int
    ) -> Avion:
        """
        Crear un nuevo avión.
        """
        return AvionRepository.create(
            modelo=modelo,
            filas=filas,
            columnas=columnas
        )
    
    @staticmethod
    def delete(avion_id: int) -> bool:
        """
        Eliminar un avión.
        """
        try:
            avion = AvionRepository.get_by_id(avion_id)
            return AvionRepository.delete(avion)
        except ValueError:
            return False
    
    @staticmethod
    def update(
        avion_id: int,
        modelo: str | None = None,
        capacidad: int | None = None,
        filas: int | None = None,
        columnas: int | None = None
    ) -> Avion | ValueError:
        """
        Actualizar un avión existente.
        """
        try:
            avion = AvionRepository.get_by_id(avion_id)
            return AvionRepository.update(
                avion=avion,
                modelo=modelo,
                capacidad=capacidad,
                filas=filas,
                columnas=columnas
            )
        except ValueError as e:
            return e