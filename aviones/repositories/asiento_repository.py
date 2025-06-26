from aviones.models import Asiento, Avion

class AsientoRepository:
    @staticmethod
    def get_all() -> list[Asiento]:
        """
        Obtener todos los asientos.
        """
        return Asiento.objects.all()
    
    @staticmethod
    def get_by_id(asiento_id: int) -> Asiento:
        """
        Obtener un asiento por su ID.
        """
        try:
            return Asiento.objects.get(pk=asiento_id)
        except Asiento.DoesNotExist:
            raise ValueError("El asiento no existe")
    
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
        return Asiento.objects.create(
            avion=avion,
            numero=numero,
            fila=fila,
            columna=columna,
            tipo=tipo
        )
    
    @staticmethod
    def delete(asiento: Asiento) -> bool:
        """
        Eliminar un asiento.
        """
        try:
            asiento.delete()
        except Asiento.DoesNotExist:
            return ValueError("El asiento no existe")
    
    @staticmethod
    def update(
        asiento: Asiento,
        numero: str | None = None,
        fila: int | None = None,
        columna: str | None = None,
        tipo: str | None = None
    ) -> Asiento:
        """
        Actualizar un asiento existente.
        """
        if numero is not None:
            asiento.numero = numero
        if fila is not None:
            asiento.fila = fila
        if columna is not None:
            asiento.columna = columna
        if tipo is not None:
            asiento.tipo = tipo
        
        asiento.save()
        return asiento
    
    @staticmethod
    def get_by_avion(avion_id: int) -> list[Asiento]:
        """
        Obtener todos los asientos de un avión específico.
        """
        return Asiento.objects.filter(avion_id=avion_id)