from aviones.models import Avion


class AvionRepository:
    @staticmethod
    def get_all() -> list[Avion]:
        """
        Obtener todos los aviones.
        """
        return Avion.objects.all()

    @staticmethod
    def get_by_id(avion_id: int) -> Avion:
        """
        Obtener un avión por su ID
        """
        try:
            return Avion.objects.get(pk=avion_id)
        except Avion.DoesNotExist:
            raise ValueError("El avión no existe")

    @staticmethod
    def create(
        modelo: str,
        filas: int,
        columnas: int
    ) -> Avion:
        """
        Crear un nuevo avión.
        """
        return Avion.objects.create(
            modelo=modelo,
            filas=filas,
            columnas=columnas
        )
    
    @staticmethod
    def delete(avion:Avion) -> bool:
        """
        Eliminar un avión.
        """
        try:
            avion.delete()
        except Avion.DoesNotExist:
            return ValueError("El avión no existe")
        
    @staticmethod
    def update(
        avion: Avion,
        modelo: str | None = None,
        capacidad: int | None = None,
        filas: int | None = None,
        columnas: int | None = None
    ) -> Avion:
        """
        Actualizar un avión existente.
        """
        if modelo is not None:
            avion.modelo = modelo
        if capacidad is not None:
            avion.capacidad = capacidad
        if filas is not None:
            avion.filas = filas
        if columnas is not None:
            avion.columnas = columnas
        avion.save()
        return avion