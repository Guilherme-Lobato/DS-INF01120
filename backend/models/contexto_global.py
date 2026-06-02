class ContextoGlobal:
    def __init__(self, bpm_inicial: int = 120):
        self.bpm_atual = bpm_inicial

    def acelerar(self):
        self.bpm_atual += 10

    def desacelerar(self):
        self.bpm_atual = max(10, self.bpm_atual - 10)
