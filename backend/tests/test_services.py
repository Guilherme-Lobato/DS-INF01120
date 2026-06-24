import unittest
from services.polifonia_service import PolifoniaService
from models.evento_musical import TipoEvento

class TestPolifoniaService(unittest.TestCase):
    def setUp(self):
        self.service = PolifoniaService()

    def test_gerar_timeline_uma_voz(self):
        texto = "A B C"
        timeline = self.service.gerar_timeline(texto)

        self.assertEqual(len(timeline), 5)
        self.assertEqual(timeline[0]['char'], 'A')
        self.assertEqual(timeline[0]['nota'], 'A')
        self.assertEqual(timeline[0]['voz_id'], 0)
        self.assertEqual(timeline[0]['beat_absoluto'], 0.0)

        self.assertEqual(timeline[1]['char'], ' ')
        self.assertEqual(timeline[1]['evento'], TipoEvento.CHANGE_VOLUME.value)
        self.assertEqual(timeline[1]['beat_absoluto'], 1.0) # A nota gastou 1 beat

        self.assertEqual(timeline[2]['char'], 'B')
        self.assertEqual(timeline[2]['nota'], 'B')
        self.assertEqual(timeline[2]['beat_absoluto'], 1.0) # O espao nǜo gasta beat

    def test_gerar_timeline_duas_vozes(self):
        texto = "A

[2] B" # Included empty line to test continue
        timeline = self.service.gerar_timeline(texto)

        # Voz 0 toca A no beat 0
        # Voz 1 toca B no beat 2 (atraso)
        self.assertEqual(len(timeline), 2)

        evento_v0 = timeline[0]
        self.assertEqual(evento_v0['char'], 'A')
        self.assertEqual(evento_v0['voz_id'], 0)
        self.assertEqual(evento_v0['beat_absoluto'], 0.0)

        evento_v1 = timeline[1]
        self.assertEqual(evento_v1['char'], 'B')
        self.assertEqual(evento_v1['voz_id'], 1)
        self.assertEqual(evento_v1['beat_absoluto'], 2.0)

    def test_gerar_timeline_bpm(self):
        texto = ">A<B"
        timeline = self.service.gerar_timeline(texto)
        self.assertEqual(len(timeline), 4)

        self.assertEqual(timeline[0]['evento'], TipoEvento.CHANGE_BPM.value)
        self.assertEqual(timeline[0]['char'], '>')
        self.assertEqual(timeline[0]['bpm'], 130)

        self.assertEqual(timeline[1]['char'], 'A')

        self.assertEqual(timeline[2]['evento'], TipoEvento.CHANGE_BPM.value)
        self.assertEqual(timeline[2]['char'], '<')
        self.assertEqual(timeline[2]['bpm'], 120)

    def test_gerar_timeline_mb(self):
        texto = "Mb"
        timeline = self.service.gerar_timeline(texto)
        self.assertEqual(len(timeline), 1)
        self.assertEqual(timeline[0]['char'], 'Mb')
        self.assertEqual(timeline[0]['nota'], 'Eb')

if __name__ == '__main__':
    unittest.main()
