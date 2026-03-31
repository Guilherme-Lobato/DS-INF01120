from regras.regra_base import RegraBase
from models.estado_musical import EstadoMusical
from models.evento_musical import EventoMusical, TipoEvento


class RegraDefault(RegraBase):
    """
    Regra coringa: qualquer caractere que nenhuma outra regra aceitou.
    - Se o caractere anterior era uma nota (A-H), repete essa nota.
    - Caso contrário, gera pausa.

    IMPORTANTE: esta regra deve ser a ÚLTIMA na lista de regras do service.
    """

    def deve_processar(self, char: str, estado: EstadoMusical) -> bool:
        # Aceita qualquer coisa — é o "else" final
        return True

    def processar(self, char: str, estado: EstadoMusical) -> EventoMusical:
        if estado.anterior_era_nota and estado.ultima_nota:
            # Repete a última nota, mas este caractere NÃO conta como nota
            evento = EventoMusical(
                tipo=TipoEvento.TOCAR_NOTA,
                char=char,
                nota=estado.ultima_nota,
                oitava=estado.oitava,
                volume=estado.volume,
                instrumento=estado.instrumento,
            )
        else:
            evento = EventoMusical(tipo=TipoEvento.PAUSA, char=char)

        estado.registrar_nao_nota()
        return evento
