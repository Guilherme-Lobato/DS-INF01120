import unittest
from fastapi.testclient import TestClient
from app import app
from unittest.mock import patch

class TestInterfaceRoute(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_enviar_form_sucesso(self):
        payload = {
            "texto": "A B C",
            "bpm": 120,
            "instrumento_inicial": 0,
            "oitava_inicial": 4,
            "volume_inicial": 64
        }
        response = self.client.post("/enviar-form", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "sucesso")
        self.assertEqual(data["bpm"], 120)
        self.assertTrue("midi_base64" in data)

    def test_enviar_form_erro_texto_vazio(self):
        payload = {
            "texto": "",
            "bpm": 120
        }
        response = self.client.post("/enviar-form", json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertTrue("O texto enviado não pode estar vazio" in response.json()["detail"])

    @patch("controllers.interface_controller.InterfaceController.processar_dados")
    def test_enviar_form_erro_interno(self, mock_processar_dados):
        # Força um erro interno para testar o bloco genérico de Exception
        mock_processar_dados.side_effect = Exception("Falha simulada no sistema")
        payload = {
            "texto": "A B C"
        }
        response = self.client.post("/enviar-form", json=payload)
        self.assertEqual(response.status_code, 500)
        self.assertTrue("Erro interno ao processar" in response.json()["detail"])
        self.assertTrue("Falha simulada" in response.json()["detail"])

if __name__ == '__main__':
    unittest.main()
