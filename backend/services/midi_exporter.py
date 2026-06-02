from midiutil import MIDIFile
from models.evento_musical import TipoEvento
import io
import base64


class MidiExporter:
    """
    Responsável por converter uma timeline de eventos musicais em um arquivo MIDI polifônico.
    """

    _NOTA_OFFSET = {
        "C": 0, "Db": 1, "D": 2, "Eb": 3, "E": 4, "F": 5, 
        "Gb": 6, "G": 7, "Ab": 8, "A": 9, "Bb": 10, "B": 11
    }

    def _calcular_nota_midi(self, nota: str, oitava: int) -> int:
        """Converte nota textual (ex: C, oitava 4) em valor numérico MIDI (0-127)."""
        offset = self._NOTA_OFFSET.get(nota, 0)
        # No MIDI padrão, C4 = 60. Logo: offset + (oitava + 1) * 12
        pitch = offset + ((oitava + 1) * 12)
        # Garante que fique entre 0 e 127
        return max(0, min(127, pitch))

    def gerar_base64(self, sequencia: list[dict], bpm_inicial: int) -> str:
        """
        Recebe a sequência gerada pelo PolifoniaService e retorna o MIDI encodado em Base64
        para ser baixado facilmente pelo frontend.
        """
        # Identificar quantas vozes existem
        vozes_ids = {e["voz_id"] for e in sequencia if "voz_id" in e}
        num_tracks = max(len(vozes_ids), 1)
        
        # Cria o arquivo MIDI com uma track por voz
        midi = MIDIFile(num_tracks)

        # Configuração inicial do BPM na track 0 (Global)
        midi.addTempo(0, 0, bpm_inicial)
            
        for evento in sequencia:
            tipo = evento.get("evento")
            tempo = evento.get("beat_absoluto", 0)
            
            # Alteração de BPM
            if tipo == TipoEvento.CHANGE_BPM.value and "bpm" in evento:
                midi.addTempo(0, tempo, evento["bpm"])
                
            # Nota Musical
            elif tipo == TipoEvento.TOCAR_NOTA.value:
                track = evento.get("voz_id", 0)
                
                # MIDI tem 16 canais (0-15). O canal 9 é reservado para percussão, então pulamos.
                canal = track % 16
                if canal == 9:
                    canal = (track + 1) % 16
                
                duracao = 1.0  # 1 beat por nota no padrão atual
                pitch = self._calcular_nota_midi(evento["nota"], evento["oitava"])
                volume = evento["volume"]
                instrumento = evento.get("instrumento", 0)

                # Definir o instrumento (Program Change)
                midi.addProgramChange(track, canal, tempo, instrumento)
                
                # Adicionar a nota
                midi.addNote(track, canal, pitch, tempo, duracao, volume)

        # Gravar em memória e converter para Base64
        with io.BytesIO() as output:
            midi.writeFile(output)
            b64 = base64.b64encode(output.getvalue()).decode("utf-8")
        
        return b64
