from dtos.interface_dto import InterfaceDTO
from services.polifonia_service import PolifoniaService
from services.midi_exporter import MidiExporter


class InterfaceController:
    """
    Camada de controle: valida entrada, chama o service e formata a resposta.
    """

    def __init__(self, polifonia_service: PolifoniaService | None = None, midi_exporter: MidiExporter | None = None):
        self.polifonia_service = polifonia_service or PolifoniaService()
        self.midi_exporter = midi_exporter or MidiExporter()

    def processar_dados(self, dados: InterfaceDTO) -> dict:
        texto = dados.texto

        if not texto or not texto.strip():
            raise ValueError("O texto enviado não pode estar vazio.")

        sequencia = self.polifonia_service.gerar_timeline(
            texto_completo=texto,
            bpm_inicial=dados.bpm
        )
        
        midi_b64 = self.midi_exporter.gerar_base64(sequencia, bpm_inicial=dados.bpm)

        return {
            "status": "sucesso",
            "bpm": dados.bpm,
            "total_eventos": len(sequencia),
            "sequencia": sequencia,
            "midi_base64": midi_b64
        }
