from pydantic import BaseModel


class InterfaceDTO(BaseModel):
    texto: str
    bpm: int = 120
    instrumento_inicial: int = 0
    oitava_inicial: int = 4
    volume_inicial: int = 64
