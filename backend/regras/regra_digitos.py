from regras.regra_base import RegraBase
from models.estado_musical import EstadoMusical
from models.evento_musical import EventoMusical, TipoEvento


class RegraDigito(RegraBase):
    """
    Dígito par: soma o valor do dígito ao instrumento atual.
    Dígito ímpar: troca para Tubular Bells (#15).
    """

    def deve_processar(self, char: str, estado: EstadoMusical) -> bool:
        return char.isdigit()

    def processar(self, char: str, estado: EstadoMusical) -> EventoMusical:
        digito = int(char)

        if digito % 2 == 0:
            estado.somar_instrumento(digito)
        else:
            estado.trocar_instrumento(15)

        estado.registrar_nao_nota()

        return EventoMusical(
            tipo=TipoEvento.CHANGE_INSTRUMENT,
            char=char,
            instrumento=estado.instrumento,
        )
