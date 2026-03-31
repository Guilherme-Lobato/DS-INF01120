from regras.regra_base import RegraBase
from models.estado_musical import EstadoMusical
from models.evento_musical import EventoMusical, TipoEvento

# Mapa: caractere → número do instrumento MIDI
_INSTRUMENTOS = {
    "!":  24,   # Bandoneon
    "O":  110,  # Gaita de Foles
    "o":  110,
    "I":  110,
    "i":  110,
    "U":  110,
    "u":  110,
    "\n": 123,  # Ondas do Mar (Seashore)
    ";":  15,   # Tubular Bells
    ",":  114,  # Agogô
}


class RegraInstrumento(RegraBase):
    """Caracteres especiais trocam o instrumento atual."""

    def deve_processar(self, char: str, estado: EstadoMusical) -> bool:
        return char in _INSTRUMENTOS

    def processar(self, char: str, estado: EstadoMusical) -> EventoMusical:
        novo_instrumento = _INSTRUMENTOS[char]
        estado.trocar_instrumento(novo_instrumento)
        estado.registrar_nao_nota()

        # Para nova linha, envia representação legível no JSON
        char_legivel = "\\n" if char == "\n" else char

        return EventoMusical(
            tipo=TipoEvento.CHANGE_INSTRUMENT,
            char=char_legivel,
            instrumento=estado.instrumento,
        )
