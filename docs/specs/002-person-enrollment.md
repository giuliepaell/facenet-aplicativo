# SPEC-002 — Cadastro de Pessoas

## 1. Objetivo

Permitir o cadastro de pessoas para reconhecimento facial, utilizando o FaceNet para gerar representações biométricas e armazenando os dados de maneira criptografada, mediante consentimento.

## 2. Tecnologias utilizadas

- **Python:** implementação da lógica.
- **Streamlit:** interface de cadastro.
- **MTCNN:** detecção e preparação do rosto.
- **FaceNet (InceptionResnetV1):** geração dos embeddings faciais.
- **SQLite:** armazenamento local dos cadastros.
- **Fernet (cryptography):** criptografia dos dados.
- **Keyring:** armazenamento da chave criptográfica no gerenciador de credenciais do sistema operacional.

## 3. Requisitos funcionais

- **RF-001:** O sistema deve permitir informar o nome da pessoa.
- **RF-002:** O sistema deve permitir enviar uma fotografia ou capturá-la pela câmera.
- **RF-003:** O sistema deve exigir confirmação de consentimento antes do cadastro.
- **RF-004:** O sistema deve aceitar somente imagens com exatamente um rosto.
- **RF-005:** O sistema deve gerar um embedding facial de 512 dimensões.
- **RF-006:** O sistema deve armazenar o nome e o embedding criptografados.
- **RF-007:** O sistema deve listar os cadastros existentes.
- **RF-008:** O sistema deve permitir excluir um cadastro.

## 4. Fluxo de cadastro

1. O usuário autenticado acessa a página "Cadastrar pessoa".
2. Informa o nome da pessoa.
3. Envia uma fotografia ou captura uma imagem pela câmera.
4. Confirma a autorização para o cadastro biométrico.
5. O aplicativo verifica se existe exatamente um rosto.
6. O MTCNN prepara a imagem para o FaceNet.
7. O FaceNet gera um embedding de 512 dimensões.
8. O nome e o embedding são criptografados.
9. O cadastro é armazenado no banco SQLite local.
10. O aplicativo apresenta uma mensagem de confirmação.

## 5. Armazenamento e segurança

Os dados são armazenados na tabela `pessoas`, do banco SQLite localizado em `dados_privados/cadastros.db`.

Cada registro possui:

- Identificador numérico.
- Nome criptografado.
- Embedding facial criptografado.
- Data e hora do cadastro.

A criptografia utiliza Fernet, e a chave é recuperada do gerenciador de credenciais do Windows por meio da biblioteca Keyring.

O diretório `dados_privados/` está incluído no `.gitignore` para evitar o envio acidental do banco de dados ao repositório Git.

## 6. Critérios de aceitação

- **CA-001:** O cadastro deve ser bloqueado quando o nome estiver vazio.
- **CA-002:** O cadastro deve ser bloqueado sem confirmação de consentimento.
- **CA-003:** O cadastro deve ser bloqueado quando nenhuma imagem for fornecida.
- **CA-004:** Imagens sem rosto ou com múltiplos rostos não devem gerar cadastros.
- **CA-005:** Um cadastro válido deve gerar um embedding de 512 dimensões.
- **CA-006:** O nome e o embedding devem ser armazenados criptografados.
- **CA-007:** O usuário autenticado deve conseguir excluir um cadastro.

## 7. Privacidade e LGPD

Os embeddings faciais são dados biométricos e devem ser tratados como dados pessoais sensíveis.

O aplicativo exige consentimento antes do cadastro e permite a exclusão dos registros.

As fotografias utilizadas para o cadastro não são armazenadas permanentemente pela implementação atual; o banco mantém o nome, o embedding e os metadados do cadastro.

A aplicação utiliza armazenamento local, sem envio dos dados biométricos a serviços externos de reconhecimento.

O consentimento e a criptografia são medidas de proteção, mas não representam, isoladamente, comprovação de conformidade integral com a LGPD.

## 8. Testes realizados

- Cadastro de pessoa com fotografia: **aprovado**.
- Geração de embedding de 512 dimensões: **aprovado**.
- Armazenamento e recuperação de cadastro criptografado: **aprovado**.
- Exclusão de cadastro pela interface: **aprovado**.
- Verificação direta da exclusão no banco SQLite: **pendente**.
- Testes específicos de cadastro sem consentimento e com múltiplos rostos: **pendentes**.