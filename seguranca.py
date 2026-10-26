from pathlib import Path
import sqlite3

from cryptography.fernet import Fernet
import keyring


SERVICO = "FaceNet_App_UFMS"
USUARIO = "chave_criptografia"

PASTA_PRIVADA = Path(__file__).parent / "dados_privados"
CAMINHO_CHAVE_ANTIGA = PASTA_PRIVADA / "chave.key"
CAMINHO_BANCO = PASTA_PRIVADA / "cadastros.db"


def existem_cadastros():
    if not CAMINHO_BANCO.exists():
        return False

    with sqlite3.connect(CAMINHO_BANCO) as conexao:
        tabela = conexao.execute(
            "SELECT name FROM sqlite_master "
            "WHERE type='table' AND name='pessoas'"
        ).fetchone()

        if tabela is None:
            return False

        quantidade = conexao.execute(
            "SELECT COUNT(*) FROM pessoas"
        ).fetchone()[0]

        return quantidade > 0


def obter_chave():
    chave_salva = keyring.get_password(SERVICO, USUARIO)

    if chave_salva is not None:
        chave = chave_salva.encode("utf-8")
        Fernet(chave)
        return chave

    # Recuperar uma chave antiga, caso exista.
    if CAMINHO_CHAVE_ANTIGA.exists():
        chave = CAMINHO_CHAVE_ANTIGA.read_bytes()

    else:
        # Não gerar outra chave se já existirem cadastros.
        if existem_cadastros():
            raise RuntimeError(
                "A chave de criptografia não foi encontrada. "
                "Existem cadastros que dependem da chave original. "
                "Nenhuma nova chave foi criada."
            )

        chave = Fernet.generate_key()

    # Validar a chave antes de armazená-la.
    Fernet(chave)

    keyring.set_password(
        SERVICO,
        USUARIO,
        chave.decode("utf-8")
    )

    confirmacao = keyring.get_password(SERVICO, USUARIO)

    if confirmacao != chave.decode("utf-8"):
        raise RuntimeError(
            "Não foi possível confirmar o armazenamento da chave."
        )

    return chave


def criptografar(dados):
    return Fernet(obter_chave()).encrypt(dados)


def descriptografar(dados):
    return Fernet(obter_chave()).decrypt(dados)