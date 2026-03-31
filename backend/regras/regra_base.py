from abc import ABC, abstractmethod
from models.estado_musical import EstadoMusical
from models.evento_musical import EventoMusical


class RegraBase(ABC):
    """
    Interface comum para todas as regras de mapeamento.

    Cada regra responde a duas perguntas:
      1. deve_processar(char, estado) → este caractere é meu?
      2. processar(char, estado)      → gere o evento e mute o estado.

    O MusicService percorre a lista de regras em ordem e usa a primeira
    que aceitar o caractere. Isso permite adicionar/remover regras sem
    alterar o service (Open-Closed Principle).
    """

    @abstractmethod
    def deve_processar(self, char: str, estado: EstadoMusical) -> bool:
        """Retorna True se esta regra se aplica ao caractere dado."""
        ...

    @abstractmethod
    def processar(self, char: str, estado: EstadoMusical) -> EventoMusical | None:
        """
        Aplica a regra: muta o estado e retorna o EventoMusical gerado.
        Pode retornar None se a regra apenas altera estado sem gerar evento.
        """
        ...
