from models.estado_musical import EstadoMusical
from models.evento_musical import EventoMusical
from regras import RegraBase, criar_regras_padrao


class MusicService:
    """
    Serviço de geração musical.

    Responsabilidade única: percorrer os caracteres do texto e delegar
    cada um para a primeira regra que aceitar processá-lo.

    As regras são injetadas via construtor (inversão de dependência),
    permitindo trocar, adicionar ou remover regras sem alterar este código.
    """

    def __init__(self, regras: list[RegraBase] | None = None):
        self.regras = regras or criar_regras_padrao()

    def gerar_sequencia(
        self,
        texto: str,
        instrumento_inicial: int = 0,
        oitava_inicial: int = 4,
        volume_inicial: int = 64,
    ) -> list[dict]:
        """
        Interpreta o texto caractere por caractere e retorna a lista
        de eventos musicais como dicionários (prontos para JSON).
        """
        estado = EstadoMusical(
            instrumento=instrumento_inicial,
            oitava=oitava_inicial,
            volume=volume_inicial,
            oitava_default=oitava_inicial,
        )

        sequencia: list[dict] = []

        for char in texto:
            evento = self._aplicar_regras(char, estado)
            if evento:
                sequencia.append(evento.to_dict())

        return sequencia

    def _aplicar_regras(self, char: str, estado: EstadoMusical) -> EventoMusical | None:
        """Percorre a lista de regras e usa a primeira que aceitar o caractere."""
        for regra in self.regras:
            if regra.deve_processar(char, estado):
                return regra.processar(char, estado)
        return None
