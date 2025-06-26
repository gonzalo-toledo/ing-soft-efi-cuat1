from aviones.models import Asiento, Avion
from aviones.repositories.asiento_repository import AsientoRepository

class AsientoService:
    @staticmethod
    def get_all() -> list[Asiento]:
        """
        Obtener todos los asientos.
        """
        return AsientoRepository.get_all()
    
    @staticmethod
    def get_by_id(asiento_id: int) -> Asiento:
        """
        Obtener un asiento por su ID.
        """
        return AsientoRepository.get_by_id(asiento_id)
    
    @staticmethod
    def create(
        avion: Avion,
        numero: str,
        fila: int,
        columna: str,
        tipo: str
    ) -> Asiento:
        """
        Crear un nuevo asiento.
        """
        return AsientoRepository.create(
            avion=avion,
            numero=numero,
            fila=fila,
            columna=columna,
            tipo=tipo
        )       
        
    @staticmethod
    def delete(asiento_id: int) -> bool:
        """
        Eliminar un asiento.
        """
        try:
            asiento = AsientoRepository.get_by_id(asiento_id)
            return AsientoRepository.delete(asiento)
        except ValueError:
            return False
    
    @staticmethod
    def update(
        asiento_id: int,
        numero: str | None = None,
        fila: int | None = None,
        columna: str | None = None,
        tipo: str | None = None
    ) -> Asiento | ValueError:
        """
        Actualizar un asiento existente.
        """
        try:
            asiento = AsientoRepository.get_by_id(asiento_id)    
            return AsientoRepository.update(
                asiento=asiento,
                numero=numero,
                fila=fila,
                columna=columna,
                tipo=tipo       
            )
        except ValueError as e:
            return e