from regras.regra_base import RegraBase
from models.estado_musical import EstadoMusical
from models.evento_musical import EventoMusical, TipoEvento

# Mapa: caractere → número do instrumento MIDI
#
# NOTA DE DESIGN (Fase 2): As vogais O/I/U (maiúsculas e minúsculas) foram
# REMOVIDAS deste mapa. Na Fase 1 elas trocavam o instrumento para Gaita de
# Foles (GM 110), mas o enunciado da Fase 2 (mapeamento da fuga) determina que
# "Outras letras (vogais O,I,U e consoantes não classificadas) seguem a regra
# original: se o caractere anterior era nota, repete a última nota; caso
# contrário, pausa." Sem a entrada aqui, esses caracteres caem em RegraDefault.
#
# O enunciado é internamente inconsistente em outros pontos; esta mudança foi
# deliberadamente isolada para reversão fácil — basta readicionar as 6 linhas
# de vogais abaixo caso o professor confirme o comportamento da Fase 1.
# Ver docs/Registros/RemocaoVogaisInstrumento.md.
_INSTRUMENTOS = {
    "!":  22,   # Harmonica (Fase 2)
    ";":  15,   # Tubular Bells
    ",":  20,   # Church Organ (Fase 2)
}


class RegraInstrumento(RegraBase):
    """Caracteres especiais trocam o instrumento atual."""

    def deve_processar(self, char: str, estado: EstadoMusical) -> bool:
        return char in _INSTRUMENTOS

    def processar(self, char: str, estado: EstadoMusical) -> EventoMusical:
        novo_instrumento = _INSTRUMENTOS[char]
        estado.trocar_instrumento(novo_instrumento)
        estado.registrar_nao_nota()

        # Para nova linha, envia representação legível no JSON
        char_legivel = "\\n" if char == "\n" else char

        return EventoMusical(
            tipo=TipoEvento.CHANGE_INSTRUMENT,
            char=char_legivel,
            instrumento=estado.instrumento,
        )
