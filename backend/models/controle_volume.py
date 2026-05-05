"""
Encapsula o eixo de variação 'volume'.

Refatoração: Extract Class a partir de EstadoMusical para tratar
o smell Divergent Change (cada eixo de variação ganha sua própria classe).
"""


class ControleVolume:
    """Estado e regras associadas ao volume atual."""

    def __init__(self, atual: int = 64, maximo: int = 127):
        self.atual = atual
        self.maximo = maximo

    def dobrar(self) -> None:
        """Dobra o volume; satura no máximo permitido."""
        self.atual = min(self.atual * 2, self.maximo)
