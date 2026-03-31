from dataclasses import dataclass, asdict
from enum import Enum


class TipoEvento(str, Enum):
    TOCAR_NOTA = "TOCAR_NOTA"
    PAUSA = "PAUSA"
    CHANGE_VOLUME = "CHANGE_VOLUME"
    CHANGE_INSTRUMENT = "CHANGE_INSTRUMENT"
    CHANGE_OCTAVE = "CHANGE_OCTAVE"


@dataclass
class EventoMusical:
    """
    Representa um único evento na sequência musical.
    Usar dataclass em vez de dict garante tipagem, autocomplete e validação.
    """

    tipo: TipoEvento
    char: str
    nota: str | None = None
    oitava: int | None = None
    volume: int | None = None
    instrumento: int | None = None

    def to_dict(self) -> dict:
        """Converte para dicionário serializável (JSON da API)."""
        resultado = {"evento": self.tipo.value, "char": self.char}
        if self.nota is not None:
            resultado["nota"] = self.nota
        if self.oitava is not None:
            resultado["oitava"] = self.oitava
        if self.volume is not None:
            resultado["volume"] = self.volume
        if self.instrumento is not None:
            resultado["instrumento"] = self.instrumento
        return resultado
