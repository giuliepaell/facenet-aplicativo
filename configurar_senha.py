
import getpass
import hashlib
import secrets
import keyring

SERVICO = "FaceNet_App_UFMS"
USUARIO = "senha_acesso"
#giulie12112002
senha = getpass.getpass("Crie uma senha de acesso: ")
confirmacao = getpass.getpass("Confirme a senha: ")

if len(senha) < 12:
    print("A senha deve ter pelo menos 12 caracteres.")
elif senha != confirmacao:
    print("As senhas não coincidem.")
else:
    salt = secrets.token_bytes(16)
    hash_senha = hashlib.pbkdf2_hmac(
        "sha256",
        senha.encode("utf-8"),
        salt,
        600_000
    )

    keyring.set_password(
        SERVICO,
        USUARIO,
        salt.hex() + ":" + hash_senha.hex()
    )

    print("Senha configurada com sucesso!")
