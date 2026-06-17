import unittest
from services.midi_exporter import MidiExporter
from models.evento_musical import TipoEvento
import base64
import io

class TestMidiExporter(unittest.TestCase):
    def setUp(self):
        self.exporter = MidiExporter()

    def test_calcular_nota_midi(self):
        self.assertEqual(self.exporter._calcular_nota_midi("C", 4), 60)
        self.assertEqual(self.exporter._calcular_nota_midi("A", 4), 69)
        self.assertEqual(self.exporter._calcular_nota_midi("C", 0), 12)
        
        self.assertEqual(self.exporter._calcular_nota_midi("C", 10), 127)

    def test_gerar_base64_vazio(self):
        timeline = []
        b64 = self.exporter.gerar_base64(timeline, 120)
        self.assertTrue(len(b64) > 0)

        try:
            base64.b64decode(b64)
        except Exception:
            self.fail("Base64 string was not correctly encoded")

    def test_gerar_base64_com_notas_e_bpm(self):
        timeline = [
            {
                "evento": TipoEvento.TOCAR_NOTA.value,
                "beat_absoluto": 0.0,
                "nota": "C",
                "oitava": 4,
                "volume": 100,
                "instrumento": 0,
                "voz_id": 0
            },
            {
                "evento": TipoEvento.CHANGE_BPM.value,
                "beat_absoluto": 1.0,
                "bpm": 140
            },
            {
                "evento": TipoEvento.TOCAR_NOTA.value,
                "beat_absoluto": 2.0,
                "nota": "D",
                "oitava": 5,
                "volume": 80,
                "instrumento": 1,
                "voz_id": 1 
            },
            {
                "evento": TipoEvento.TOCAR_NOTA.value,
                "beat_absoluto": 3.0,
                "nota": "E",
                "oitava": 4,
                "volume": 100,
                "instrumento": 0,
                "voz_id": 9 
            }
        ]
        
        b64 = self.exporter.gerar_base64(timeline, 120)
        self.assertTrue(len(b64) > 0)

if __name__ == '__main__':
    unittest.main()
