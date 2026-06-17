import unittest
from models.estado_musical import EstadoMusical
from models.evento_musical import TipoEvento
from regras.regra_notas import RegraNota
from regras.regra_pausas import RegraPausa
from regras.regra_volume import RegraVolume
from regras.regra_instrumentos import RegraInstrumento
from regras.regra_digitos import RegraDigito
from regras.regra_oitava import RegraOitava
from regras.regra_bpm import RegraBpm
from regras.regra_default import RegraDefault

class TestRegras(unittest.TestCase):
    def setUp(self):
        self.estado = EstadoMusical()

    def test_regra_nota(self):
        regra = RegraNota()
        self.assertTrue(regra.deve_processar('A', self.estado))
        self.assertFalse(regra.deve_processar('Z', self.estado))
        
        evento = regra.processar('A', self.estado)
        self.assertEqual(evento.tipo, TipoEvento.TOCAR_NOTA)
        self.assertEqual(evento.nota, 'A')
        self.assertTrue(self.estado.anterior_era_nota)
        self.assertEqual(self.estado.ultima_nota, 'A')

    def test_regra_pausa(self):
        regra = RegraPausa()
        self.assertTrue(regra.deve_processar('a', self.estado))
        self.assertFalse(regra.deve_processar('A', self.estado))
        
        evento = regra.processar('a', self.estado)
        self.assertEqual(evento.tipo, TipoEvento.PAUSA)
        self.assertFalse(self.estado.anterior_era_nota)

    def test_regra_volume(self):
        regra = RegraVolume()
        self.assertTrue(regra.deve_processar(' ', self.estado))
        
        self.estado.volume = 40
        evento = regra.processar(' ', self.estado)
        self.assertEqual(evento.tipo, TipoEvento.CHANGE_VOLUME)
        self.assertEqual(self.estado.volume, 80)
        self.assertFalse(self.estado.anterior_era_nota)

    def test_regra_instrumentos(self):
        regra = RegraInstrumento()
        self.assertTrue(regra.deve_processar('!', self.estado))
        self.assertTrue(regra.deve_processar('I', self.estado))
        self.assertTrue(regra.deve_processar(';', self.estado))
        self.assertTrue(regra.deve_processar(',', self.estado))
        
        evento = regra.processar('!', self.estado)
        self.assertEqual(evento.tipo, TipoEvento.CHANGE_INSTRUMENT)
        self.assertEqual(self.estado.instrumento, 22)

    def test_regra_digitos(self):
        regra = RegraDigito()
        self.assertTrue(regra.deve_processar('2', self.estado))
        self.assertTrue(regra.deve_processar('3', self.estado))
        self.assertFalse(regra.deve_processar('A', self.estado))
        
        # Par soma
        self.estado.instrumento = 5
        evento = regra.processar('2', self.estado)
        self.assertEqual(self.estado.instrumento, 7)
        
        # Ímpar Tubular Bells (15)
        evento2 = regra.processar('3', self.estado)
        self.assertEqual(self.estado.instrumento, 15)

    def test_regra_oitava(self):
        regra = RegraOitava()
        self.assertTrue(regra.deve_processar('?', self.estado))
        self.assertTrue(regra.deve_processar('.', self.estado))
        self.assertTrue(regra.deve_processar('V', self.estado))
        
        self.estado.oitava = 4
        evento = regra.processar('?', self.estado)
        self.assertEqual(self.estado.oitava, 5)
        
        evento2 = regra.processar('V', self.estado)
        self.assertEqual(self.estado.oitava, 4)

    def test_regra_bpm(self):
        regra = RegraBpm()
        self.assertTrue(regra.deve_processar('>', self.estado))
        self.assertTrue(regra.deve_processar('<', self.estado))
        
        evento = regra.processar('>', self.estado)
        self.assertEqual(evento.tipo, TipoEvento.CHANGE_BPM)

    def test_regra_default(self):
        regra = RegraDefault()
        self.assertTrue(regra.deve_processar('Z', self.estado))
        
        # Sem nota anterior
        evento = regra.processar('Z', self.estado)
        self.assertEqual(evento.tipo, TipoEvento.PAUSA)
        
        # Com nota anterior
        self.estado.registrar_nota('A')
        evento2 = regra.processar('Z', self.estado)
        self.assertEqual(evento2.tipo, TipoEvento.TOCAR_NOTA)
        self.assertEqual(evento2.nota, 'A')

if __name__ == '__main__':
    unittest.main()
