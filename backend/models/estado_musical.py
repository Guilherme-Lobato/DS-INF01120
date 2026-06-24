"""
EstadoMusical — Versão refatorada.

Antes: classe com 4 eixos de mudança independentes (oitava, volume,
instrumento e histórico de notas), caracterizando o smell
Divergent Change.

Depois: fachada coesa que agrega três controles especializados
(ControleOitava, ControleVolume, HistoricoNotas) e mantém o instrumento
como atributo simples (sua lógica é trivial).

A API pública foi preservada via @property e métodos de delegação,
de modo que NENHUMA das 7 regras (RegraNota, RegraPausa, RegraVolume,
RegraInstrumento, RegraDigito, RegraOitava, RegraDefault) precisou
ser alterada.
"""
from models.controle_oitava import ControleOitava
from models.controle_volume import ControleVolume
from models.historico_notas import HistoricoNotas


class EstadoMusical:
    """
    Encapsula o estado local (por voz) durante a interpretação do texto.
    """

    def __init__(
        self,
        instrumento: int = 0,
        oitava: int = 4,
        volume: int = 64,
        oitava_default: int = 4,
        oitava_max: int = 9,
        oitava_min: int = 0,
        volume_max: int = 127,
    ):
        self._oitava = ControleOitava(
            atual=oitava, default=oitava_default, maximo=oitava_max, minimo=oitava_min
        )
        self._volume = ControleVolume(atual=volume, maximo=volume_max)
        self._historico = HistoricoNotas()
        self.instrumento = instrumento
        self.oitava_default = oitava_default
        self.oitava_max = oitava_max
        self.oitava_min = oitava_min
        self.volume_max = volume_max

    # ── Propriedades de leitura: preservam a API antiga ──

    @property
    def oitava(self) -> int:
        return self._oitava.atual

    @oitava.setter
    def oitava(self, valor: int) -> None:
        self._oitava.atual = valor

    @property
    def volume(self) -> int:
        return self._volume.atual

    @volume.setter
    def volume(self, valor: int) -> None:
        self._volume.atual = valor

    @property
    def ultima_nota(self) -> str | None:
        return self._historico.ultima

    @property
    def anterior_era_nota(self) -> bool:
        return self._historico.anterior_era_nota

    # ── Mutações: cada uma delega para o controle responsável ──

    def subir_oitava(self) -> None:
        self._oitava.subir()

    def dobrar_volume(self) -> None:
        self._volume.dobrar()

    def diminuir_oitava(self) -> None:
        self._oitava.diminuir()

    def trocar_instrumento(self, novo: int) -> None:
        self.instrumento = novo % 128

    def somar_instrumento(self, valor: int) -> None:
        self.instrumento = (self.instrumento + valor) % 128

    def registrar_nota(self, nota: str) -> None:
        self._historico.registrar_nota(nota)

    def registrar_nao_nota(self) -> None:
        self._historico.registrar_nao_nota()
