import unittest
import numpy as np

from reconhecimento import reconhecer_pessoa


class TestReconhecimento(unittest.TestCase):

    def test_pessoa_desconhecida_sem_cadastros(self):
        embedding = np.ones(512, dtype=np.float32)

        nome, similaridade = reconhecer_pessoa(
            embedding,
            [],
            limiar=0.8
        )

        self.assertEqual(nome, "Desconhecido")
        self.assertEqual(similaridade, 0.0)

    def test_pessoa_conhecida(self):
        embedding = np.ones(512, dtype=np.float32)

        pessoas = [
            (1, "Pessoa Teste", embedding.copy())
        ]

        nome, similaridade = reconhecer_pessoa(
            embedding,
            pessoas,
            limiar=0.8
        )

        self.assertEqual(nome, "Pessoa Teste")
        self.assertAlmostEqual(similaridade, 1.0, places=5)
    def test_pessoa_desconhecida_com_cadastro(self):
        embedding_cadastrado = np.zeros(512, dtype=np.float32)
        embedding_cadastrado[0] = 1.0

        embedding_consulta = np.zeros(512, dtype=np.float32)
        embedding_consulta[1] = 1.0

        pessoas = [
            (1, "Pessoa Teste", embedding_cadastrado)
        ]

        nome, similaridade = reconhecer_pessoa(
            embedding_consulta,
            pessoas,
            limiar=0.8
        )

        self.assertEqual(nome, "Desconhecido")
        self.assertAlmostEqual(similaridade, 0.0, places=5)
    def test_embedding_com_dimensao_incorreta(self):
        embedding_invalido = np.ones(128, dtype=np.float32)
        embedding_valido = np.ones(512, dtype=np.float32)

        pessoas = [
            (1, "Pessoa Teste", embedding_valido)
        ]

        with self.assertRaises(ValueError):
            reconhecer_pessoa(
                embedding_invalido,
                pessoas,
                limiar=0.8
            )
    def test_embedding_zerado(self):
        embedding_zerado = np.zeros(512, dtype=np.float32)
        embedding_valido = np.ones(512, dtype=np.float32)

        pessoas = [
            (1, "Pessoa Teste", embedding_valido)
        ]

        with self.assertRaises(ValueError):
            reconhecer_pessoa(
                embedding_zerado,
                pessoas,
                limiar=0.8
            )
if __name__ == "__main__":
    
    unittest.main()
