import unittest
from unittest.mock import patch

from cryptography.fernet import Fernet
from seguranca import criptografar, descriptografar


class TestSeguranca(unittest.TestCase):

    def test_criptografia_e_descriptografia(self):
        chave_teste = Fernet.generate_key()
        dados_originais = b"Dados ficticios para teste"

        with patch("seguranca.obter_chave", return_value=chave_teste):
            dados_criptografados = criptografar(dados_originais)
            dados_recuperados = descriptografar(dados_criptografados)

        self.assertNotEqual(dados_criptografados, dados_originais)
        self.assertEqual(dados_recuperados, dados_originais)


if __name__ == "__main__":
    unittest.main()
    