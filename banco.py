
import sqlite3
from pathlib import Path
import numpy as np

from seguranca import criptografar, descriptografar


PASTA_PRIVADA = Path(__file__).parent / "dados_privados"
CAMINHO_BANCO = PASTA_PRIVADA / "cadastros.db"

def conectar():
    PASTA_PRIVADA.mkdir(parents=True, exist_ok=True)

    conexao = sqlite3.connect(CAMINHO_BANCO)
    conexao.execute("PRAGMA secure_delete = ON")

    return conexao

def criar_banco():
    with conectar() as conexao:
        conexao.execute("""
            CREATE TABLE IF NOT EXISTS pessoas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                embedding BLOB NOT NULL,
                data_cadastro TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)


def listar_pessoas():
    with conectar() as conexao:
        registros = conexao.execute(
            "SELECT id, nome, data_cadastro "
            "FROM pessoas ORDER BY id"
        ).fetchall()

    pessoas = []

    for pessoa_id, nome_criptografado, data in registros:
        nome = descriptografar(
            nome_criptografado.encode("utf-8")
        ).decode("utf-8")

        pessoas.append((pessoa_id, nome, data))

    return pessoas


def excluir_pessoa(pessoa_id):
    with conectar() as conexao:
        cursor = conexao.execute(
            "DELETE FROM pessoas WHERE id = ?",
            (pessoa_id,)
        )
        return cursor.rowcount > 0


def cadastrar_pessoa(nome, embedding):
    if not nome.strip():
        raise ValueError("O nome não pode estar vazio.")

    vetor = np.asarray(embedding, dtype=np.float32)

    if vetor.shape != (512,):
        raise ValueError("O embedding deve ter 512 dimensões.")

    if not np.isfinite(vetor).all():
        raise ValueError("O embedding contém valores inválidos.")

    # Criptografar o nome
    nome_criptografado = criptografar(
        nome.strip().encode("utf-8")
    ).decode("utf-8")

    # Criptografar o embedding
    embedding_criptografado = criptografar(
        vetor.tobytes()
    )

    with conectar() as conexao:
        cursor = conexao.execute(
            "INSERT INTO pessoas (nome, embedding) "
            "VALUES (?, ?)",
            (nome_criptografado, embedding_criptografado)
        )

        return cursor.lastrowid


def obter_embeddings():
    with conectar() as conexao:
        registros = conexao.execute(
            "SELECT id, nome, embedding FROM pessoas"
        ).fetchall()

    pessoas = []

    for pessoa_id, nome_criptografado, dados_criptografados in registros:

        # Recuperar nome
        nome = descriptografar(
            nome_criptografado.encode("utf-8")
        ).decode("utf-8")

        # Recuperar embedding
        dados = descriptografar(dados_criptografados)

        embedding = np.frombuffer(
            dados,
            dtype=np.float32
        ).copy()

        if embedding.shape != (512,):
            raise ValueError("Embedding armazenado inválido.")

        pessoas.append(
            (pessoa_id, nome, embedding)
        )

    return pessoas
