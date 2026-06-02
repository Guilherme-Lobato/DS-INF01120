"""
Encapsula o eixo de variação 'oitava'.

Refatoração: Extract Class a partir de EstadoMusical para tratar
o smell Divergent Change (cada eixo de variação ganha sua própria classe).
"""


class ControleOitava:
    """Estado e regras associadas à oitava atual."""

    def __init__(self, atual: int = 4, default: int = 4, maximo: int = 9):
        self.atual = atual
        self.default = default
        self.maximo = maximo

    def subir(self) -> None:
        """Sobe a oitava em 1; volta ao default ao ultrapassar o máximo."""
        self.atual += 1
        if self.atual > self.maximo:
            self.atual = self.default
