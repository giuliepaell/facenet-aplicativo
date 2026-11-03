import unittest
from unittest.mock import patch

from autenticacao import verificar_senha


class TestAutenticacao(unittest.TestCase):

    def test_senha_incorreta(self):
        with patch(
            "autenticacao.keyring.get_password",
            return_value=None
        ):
            resultado = verificar_senha("senha_incorreta_123")

        self.assertFalse(resultado)


if __name__ == "__main__":
    unittest.main()