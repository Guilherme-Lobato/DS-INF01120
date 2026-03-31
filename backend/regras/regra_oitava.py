from regras.regra_base import RegraBase
from models.estado_musical import EstadoMusical
from models.evento_musical import EventoMusical, TipoEvento


class RegraOitava(RegraBase):
    """? e . aumentam a oitava em 1 (volta ao default se exceder o máximo)."""

    def deve_processar(self, char: str, estado: EstadoMusical) -> bool:
        return char in ("?", ".")

    def processar(self, char: str, estado: EstadoMusical) -> EventoMusical:
        estado.subir_oitava()
        estado.registrar_nao_nota()

        return EventoMusical(
            tipo=TipoEvento.CHANGE_OCTAVE,
            char=char,
            oitava=estado.oitava,
        )
