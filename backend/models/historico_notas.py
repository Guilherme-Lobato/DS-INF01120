"""
Rastreia se o caractere processado anteriormente foi uma nota
e qual foi a última nota tocada.

Refatoração: Extract Class a partir de EstadoMusical para tratar
o smell Divergent Change (cada eixo de variação ganha sua própria classe).
"""


class HistoricoNotas:
    """Histórico mínimo necessário para a regra de 'repetir última nota'."""

    def __init__(self):
        self.ultima: str | None = None
        self.anterior_era_nota: bool = False

    def registrar_nota(self, nota: str) -> None:
        """Chamado após tocar uma nota para atualizar o histórico."""
        self.ultima = nota
        self.anterior_era_nota = True

    def registrar_nao_nota(self) -> None:
        """Chamado quando o caractere processado NÃO é uma nota direta."""
        self.anterior_era_nota = False
