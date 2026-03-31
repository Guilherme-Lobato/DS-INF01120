from regras.regra_base import RegraBase
from models.estado_musical import EstadoMusical
from models.evento_musical import EventoMusical, TipoEvento

_PAUSAS = set("abcdefgh")


class RegraPausa(RegraBase):
    """Letras minúsculas a-h geram silêncio/pausa."""

    def deve_processar(self, char: str, estado: EstadoMusical) -> bool:
        return char in _PAUSAS

    def processar(self, char: str, estado: EstadoMusical) -> EventoMusical:
        estado.registrar_nao_nota()
        return EventoMusical(tipo=TipoEvento.PAUSA, char=char)
