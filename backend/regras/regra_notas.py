from regras.regra_base import RegraBase
from models.estado_musical import EstadoMusical
from models.evento_musical import EventoMusical, TipoEvento

# Mapeamento de letra maiúscula para nome da nota
_NOTAS = {
    "A": "A",   # Lá
    "B": "B",   # Si
    "C": "C",   # Dó
    "D": "D",   # Ré
    "E": "E",   # Mi
    "F": "F",   # Fá
    "G": "G",   # Sol
    "H": "Bb",  # Si Bemol
    "Mb": "Eb", # Mi Bemol
}


class RegraNota(RegraBase):
    """Letras A-G tocam a nota correspondente; H toca Si Bemol."""

    def deve_processar(self, char: str, estado: EstadoMusical) -> bool:
        return char in _NOTAS

    def processar(self, char: str, estado: EstadoMusical) -> EventoMusical:
        nota = _NOTAS[char]
        estado.registrar_nota(nota)
        return EventoMusical(
            tipo=TipoEvento.TOCAR_NOTA,
            char=char,
            nota=nota,
            oitava=estado.oitava,
            volume=estado.volume,
            instrumento=estado.instrumento,
        )
