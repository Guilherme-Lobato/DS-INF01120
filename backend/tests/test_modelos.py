import unittest
from models.contexto_global import ContextoGlobal
from models.estado_musical import EstadoMusical
from models.evento_musical import EventoMusical, TipoEvento
from models.voz import Voz

class TestModelos(unittest.TestCase):
    def test_contexto_global_acelerar(self):
        contexto = ContextoGlobal(bpm_inicial=120)
        contexto.acelerar()
        self.assertEqual(contexto.bpm_atual, 130)

    def test_contexto_global_desacelerar(self):
        contexto = ContextoGlobal(bpm_inicial=120)
        contexto.desacelerar()
        self.assertEqual(contexto.bpm_atual, 110)

    def test_contexto_global_desacelerar_limite(self):
        contexto = ContextoGlobal(bpm_inicial=15)
        contexto.desacelerar()
        self.assertEqual(contexto.bpm_atual, 10)

    def test_estado_musical_inicializacao(self):
        estado = EstadoMusical()
        self.assertEqual(estado.oitava, 4)
        self.assertEqual(estado.volume, 64)
        self.assertEqual(estado.instrumento, 0)
        self.assertIsNone(estado.ultima_nota)
        self.assertFalse(estado.anterior_era_nota)

    def test_estado_musical_mutacoes(self):
        estado = EstadoMusical()
        estado.subir_oitava()
        self.assertEqual(estado.oitava, 5)
        
        # Testar subir acima do máximo
        estado.oitava = 9
        estado.subir_oitava()
        self.assertEqual(estado.oitava, 4)  # Volta ao default
        
        estado.diminuir_oitava()
        self.assertEqual(estado.oitava, 3)
        
        # Testar diminuir abaixo do mínimo
        estado.oitava = 0
        estado.diminuir_oitava()
        self.assertEqual(estado.oitava, 4)  # Volta ao default
        
        estado.dobrar_volume()
        self.assertEqual(estado.volume, 127) # MAX is 127
        
        estado.trocar_instrumento(130)
        self.assertEqual(estado.instrumento, 2) # modulo 128
        
        estado.somar_instrumento(10)
        self.assertEqual(estado.instrumento, 12)
        
        estado.registrar_nota('A')
        self.assertEqual(estado.ultima_nota, 'A')
        self.assertTrue(estado.anterior_era_nota)
        
        estado.registrar_nao_nota()
        self.assertEqual(estado.ultima_nota, 'A')
        self.assertFalse(estado.anterior_era_nota)

    def test_voz_atraso_invalido(self):
        voz = Voz(id_voz=0, texto_original="[inv] A B C")
        self.assertEqual(voz.atraso_beats, 0)
        self.assertEqual(voz.texto_processar, "[inv] A B C")

    def test_voz_sem_fechar_colchete(self):
        voz = Voz(id_voz=0, texto_original="[4 A B C")
        self.assertEqual(voz.atraso_beats, 0)
        self.assertEqual(voz.texto_processar, "[4 A B C")

if __name__ == '__main__':
    unittest.main()
