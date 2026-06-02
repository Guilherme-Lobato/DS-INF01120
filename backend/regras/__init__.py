from .regra_base import RegraBase
from .regra_notas import RegraNota
from .regra_pausas import RegraPausa
from .regra_volume import RegraVolume
from .regra_instrumentos import RegraInstrumento
from .regra_digitos import RegraDigito
from .regra_oitava import RegraOitava
from .regra_bpm import RegraBpm
from .regra_default import RegraDefault


def criar_regras_padrao() -> list[RegraBase]:
    """
    Retorna a lista de regras na ordem correta de avaliação.
    RegraDefault DEVE ser a última (é o 'else').
    """
    return [
        RegraNota(),
        RegraPausa(),
        RegraVolume(),
        RegraInstrumento(),
        RegraDigito(),
        RegraOitava(),
        RegraBpm(),
        RegraDefault(),  # sempre por último
    ]