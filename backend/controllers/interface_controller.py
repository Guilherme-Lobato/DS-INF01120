from dtos.interface_dto import InterfaceDTO
from services.music_service import MusicService


class InterfaceController:
    """
    Camada de controle: valida entrada, chama o service e formata a resposta.
    """

    def __init__(self, music_service: MusicService | None = None):
        self.music_service = music_service or MusicService()

    def processar_dados(self, dados: InterfaceDTO) -> dict:
        texto = dados.texto

        if not texto or not texto.strip():
            raise ValueError("O texto enviado não pode estar vazio.")

        sequencia = self.music_service.gerar_sequencia(
            texto=texto,
            instrumento_inicial=dados.instrumento_inicial,
            oitava_inicial=dados.oitava_inicial,
            volume_inicial=dados.volume_inicial,
        )

        return {
            "status": "sucesso",
            "bpm": dados.bpm,
            "total_eventos": len(sequencia),
            "sequencia": sequencia,
        }
