from regras.regra_base import RegraBase
from models.estado_musical import EstadoMusical
from models.evento_musical import EventoMusical, TipoEvento


class RegraVolume(RegraBase):
    """Espaço dobra o volume (ou coloca no máximo)."""

    def deve_processar(self, char: str, estado: EstadoMusical) -> bool:
        return char == " "

    def processar(self, char: str, estado: EstadoMusical) -> EventoMusical:
        estado.dobrar_volume()
        estado.registrar_nao_nota()
        return EventoMusical(
            tipo=TipoEvento.CHANGE_VOLUME,
            char=char,
            volume=estado.volume,
        )
