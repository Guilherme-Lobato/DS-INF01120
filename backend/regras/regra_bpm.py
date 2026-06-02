from regras.regra_base import RegraBase
from models.estado_musical import EstadoMusical
from models.evento_musical import EventoMusical, TipoEvento

class RegraBpm(RegraBase):
    """Caracteres > e < alteram o andamento (BPM) globalmente."""

    def deve_processar(self, char: str, estado: EstadoMusical) -> bool:
        return char in (">", "<")

    def processar(self, char: str, estado: EstadoMusical) -> EventoMusical:
        estado.registrar_nao_nota()
        return EventoMusical(
            tipo=TipoEvento.CHANGE_BPM,
            char=char
        )