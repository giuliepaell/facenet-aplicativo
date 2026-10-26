
import numpy as np


def similaridade_cosseno(embedding1, embedding2):
    vetor1 = np.asarray(embedding1, dtype=np.float32)
    vetor2 = np.asarray(embedding2, dtype=np.float32)

    if vetor1.shape != (512,) or vetor2.shape != (512,):
        raise ValueError("Os embeddings devem ter 512 dimensões.")

    norma1 = np.linalg.norm(vetor1)
    norma2 = np.linalg.norm(vetor2)

    if norma1 == 0 or norma2 == 0:
        raise ValueError("Não é possível comparar vetores nulos.")

    return float(np.dot(vetor1, vetor2) / (norma1 * norma2))


def encontrar_mais_semelhante(embedding_consulta, pessoas):
    melhor_pessoa = None
    maior_similaridade = -1.0

    for pessoa_id, nome, embedding_cadastrado in pessoas:
        similaridade = similaridade_cosseno(
            embedding_consulta,
            embedding_cadastrado
        )

        if similaridade > maior_similaridade:
            maior_similaridade = similaridade
            melhor_pessoa = (pessoa_id, nome)

    return melhor_pessoa, maior_similaridade

def reconhecer_pessoa(embedding_consulta, pessoas, limiar):
    if not pessoas:
        return "Desconhecido", 0.0

    pessoa, similaridade = encontrar_mais_semelhante(
        embedding_consulta,
        pessoas
    )

    if similaridade >= limiar:
        return pessoa[1], similaridade

    return "Desconhecido", similaridade
