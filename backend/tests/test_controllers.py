import unittest
from controllers.interface_controller import InterfaceController
from dtos.interface_dto import InterfaceDTO

class TestInterfaceController(unittest.TestCase):
    def setUp(self):
        self.controller = InterfaceController()

    def test_processar_dados_sucesso(self):
        dto = InterfaceDTO(texto="A B C", bpm=120)
        resultado = self.controller.processar_dados(dto)
        
        self.assertEqual(resultado["status"], "sucesso")
        self.assertEqual(resultado["bpm"], 120)
        self.assertEqual(resultado["total_eventos"], 5) # A, volume(space), B, volume(space), C
        self.assertTrue(len(resultado["midi_base64"]) > 0)
        self.assertTrue(len(resultado["sequencia"]) > 0)

    def test_processar_dados_texto_vazio(self):
        dto = InterfaceDTO(texto="   ", bpm=120)
        with self.assertRaises(ValueError) as context:
            self.controller.processar_dados(dto)
        
        self.assertTrue("O texto enviado não pode estar vazio" in str(context.exception))

if __name__ == '__main__':
    unittest.main()
