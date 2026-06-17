from pydantic import BaseModel


class InterfaceDTO(BaseModel):
    texto: str
    bpm: int = 120
