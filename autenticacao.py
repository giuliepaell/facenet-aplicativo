
import hashlib
import hmac
import keyring

SERVICO = "FaceNet_App_UFMS"
USUARIO = "senha_acesso"


def verificar_senha(senha_digitada):
    registro = keyring.get_password(SERVICO, USUARIO)

    if registro is None:
        return False

    salt_hex, hash_hex = registro.split(":")

    salt = bytes.fromhex(salt_hex)
    hash_esperado = bytes.fromhex(hash_hex)

    hash_digitado = hashlib.pbkdf2_hmac(
        "sha256",
        senha_digitada.encode("utf-8"),
        salt,
        600_000
    )

    return hmac.compare_digest(
        hash_digitado,
        hash_esperado
    )
