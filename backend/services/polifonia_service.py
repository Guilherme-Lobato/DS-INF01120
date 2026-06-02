from models.voz import Voz
from models.evento_musical import EventoMusical, TipoEvento
from models.contexto_global import ContextoGlobal
from regras import RegraBase, criar_regras_padrao


class PolifoniaService:
    """
    Maestro que gerencia múltiplas vozes (Fuga/Polifonia) e calcula a timeline.
    """

    def __init__(self, regras: list[RegraBase] | None = None):
        self.regras = regras or criar_regras_padrao()

    def gerar_timeline(self, texto_completo: str, bpm_inicial: int = 120) -> list[dict]:
        """
        Recebe o texto completo, divide em linhas (vozes) e gera a timeline
        absoluta com todos os eventos ordenados cronologicamente.
        """
        vozes = self._separar_vozes(texto_completo)
        todos_eventos = []

        for voz in vozes:
            eventos_voz = self._processar_voz(voz)
            todos_eventos.extend(eventos_voz)

        # Ordenar todos os eventos pelo beat absoluto de forma cronológica
        # Eventos do mesmo beat devem manter a ordem em que foram gerados (Python sort é estável)
        todos_eventos.sort(key=lambda e: e.beat_absoluto)

        # Segunda passagem: resolver o Contexto Global (ex: BPM) em ordem cronológica
        contexto = ContextoGlobal(bpm_inicial=bpm_inicial)
        for evento in todos_eventos:
            if evento.tipo == TipoEvento.CHANGE_BPM:
                if evento.char == ">":
                    contexto.acelerar()
                elif evento.char == "<":
                    contexto.desacelerar()
                evento.bpm = contexto.bpm_atual

        return [e.to_dict() for e in todos_eventos]

    def _separar_vozes(self, texto: str) -> list[Voz]:
        linhas = texto.split('\n')
        vozes = []
        id_voz = 0
        for linha in linhas:
            if linha.strip() == "":
                continue
            vozes.append(Voz(id_voz=id_voz, texto_original=linha))
            id_voz += 1
        return vozes

    def _processar_voz(self, voz: Voz) -> list[EventoMusical]:
        """Processa os caracteres de uma única voz, calculando seu beat_absoluto."""
        eventos = []
        beat_atual = float(voz.atraso_beats)

        texto = voz.texto_processar
        i = 0
        n = len(texto)
        while i < n:
            char = texto[i]

            # Lookahead para tratar 'Mb' como um único caractere musical
            if char == "M" and i + 1 < n and texto[i+1] == "b":
                char = "Mb"
                i += 1  # Pula o 'b' na próxima iteração

            evento = self._aplicar_regras(char, voz)
            if evento:
                evento.voz_id = voz.id_voz
                evento.beat_absoluto = beat_atual
                
                # Se for nota ou pausa, avança 1 beat
                if evento.tipo in (TipoEvento.TOCAR_NOTA, TipoEvento.PAUSA):
                    beat_atual += 1.0
                
                eventos.append(evento)
            
            i += 1

        return eventos

    def _aplicar_regras(self, char: str, voz: Voz) -> EventoMusical | None:
        """Delega o caractere para a regra correta."""
        for regra in self.regras:
            if regra.deve_processar(char, voz.estado):
                return regra.processar(char, voz.estado)
        return None
