import uuid
from reservas.repositories.boleto_repository import BoletoRepository

class BoletoService:

    @staticmethod
    def emitir_boleto(data):
        # Generamos un código único
        codigo = BoletoService._generar_codigo_unico()
        data['codigo_barra'] = codigo
        return BoletoRepository.create(**data)

    @staticmethod
    def _generar_codigo_unico():
        # Generamos un código de 12 caracteres unico
        return str(uuid.uuid4()).replace('-', '')[:12].upper()

    @staticmethod
    def anular_boleto(boleto_id):
        boleto = BoletoRepository.get_by_id(boleto_id)
        boleto.estado = 'Anulado'
        boleto.save()
        return boleto