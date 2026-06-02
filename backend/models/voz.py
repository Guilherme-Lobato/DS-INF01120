from models.estado_musical import EstadoMusical

class Voz:
    def __init__(self, id_voz: int, texto_original: str):
        self.id_voz = id_voz
        self.texto_original = texto_original
        self.atraso_beats = 0
        self.estado = EstadoMusical()
        self.inicializar_atributos_base()
        self.texto_processar = self.extrair_atraso()

    def inicializar_atributos_base(self):
        # Ciclo de oitavas: 0=6, 1=5, 2=4, 3=3
        ciclo = self.id_voz % 4
        oitavas = [6, 5, 4, 3]
        volumes = [100, 80, 60, 40]
        instrumentos = [6, 20, 0, 70] # Cravo, Órgão, Piano, Fagote
        
        self.estado.oitava = oitavas[ciclo]
        self.estado.oitava_default = oitavas[ciclo]
        self.estado.volume = volumes[ciclo]
        self.estado.instrumento = instrumentos[ciclo]

    def extrair_atraso(self) -> str:
        texto = self.texto_original.strip()
        if texto.startswith("["):
            fim_colchete = texto.find("]")
            if fim_colchete != -1:
                try:
                    self.atraso_beats = int(texto[1:fim_colchete])
                    return texto[fim_colchete+1:].strip()
                except ValueError:
                    pass
        return texto
