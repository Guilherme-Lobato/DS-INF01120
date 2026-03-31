class EstadoMusical:
    """
    Encapsula o estado mutável durante a interpretação do texto.
    Cada chamada de geração cria uma instância nova, garantindo isolamento.
    """

    def __init__(
        self,
        instrumento: int = 0,
        oitava: int = 4,
        volume: int = 64,
        oitava_default: int = 4,
        oitava_max: int = 9,
        volume_max: int = 127,
    ):
        self.instrumento = instrumento
        self.oitava = oitava
        self.volume = volume
        self.oitava_default = oitava_default
        self.oitava_max = oitava_max
        self.volume_max = volume_max
        self.ultima_nota: str | None = None
        self.anterior_era_nota: bool = False

    # ── Métodos de mutação com lógica de negócio embutida ──

    def dobrar_volume(self) -> None:
        self.volume = min(self.volume * 2, self.volume_max)

    def subir_oitava(self) -> None:
        self.oitava += 1
        if self.oitava > self.oitava_max:
            self.oitava = self.oitava_default

    def trocar_instrumento(self, novo: int) -> None:
        self.instrumento = novo % 128

    def somar_instrumento(self, valor: int) -> None:
        self.instrumento = (self.instrumento + valor) % 128

    def registrar_nota(self, nota: str) -> None:
        """Chamado após tocar uma nota para atualizar o histórico."""
        self.ultima_nota = nota
        self.anterior_era_nota = True

    def registrar_nao_nota(self) -> None:
        """Chamado quando o caractere processado NÃO é uma nota direta."""
        self.anterior_era_nota = False
