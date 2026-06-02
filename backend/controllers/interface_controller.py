from dtos.interface_dto import InterfaceDTO
from services.polifonia_service import PolifoniaService


class InterfaceController:
    """
    Camada de controle: valida entrada, chama o service e formata a resposta.
    """

    def __init__(self, polifonia_service: PolifoniaService | None = None):
        self.polifonia_service = polifonia_service or PolifoniaService()

    def processar_dados(self, dados: InterfaceDTO) -> dict:
        texto = dados.texto

        if not texto or not texto.strip():
            raise ValueError("O texto enviado não pode estar vazio.")

        sequencia = self.polifonia_service.gerar_timeline(
            texto_completo=texto
        )

        return {
            "status": "sucesso",
            "bpm": dados.bpm,
            "total_eventos": len(sequencia),
            "sequencia": sequencia,
        }
