# FaceNet — Aplicativo de Reconhecimento Facial

Aplicativo acadêmico de reconhecimento facial desenvolvido em Python, utilizando **MTCNN** para detecção de rostos e **FaceNet** para geração de embeddings faciais.

O projeto foi desenvolvido como parte de uma atividade universitária de Inteligência Artificial, com foco em reconhecimento facial, avaliação de modelos e proteção de dados biométricos.

## Funcionalidades

- Autenticação por senha.
- Cadastro de pessoas mediante confirmação de consentimento.
- Envio de fotografias nos formatos JPG, JPEG e PNG.
- Captura de fotografias pela câmera.
- Detecção facial utilizando MTCNN.
- Geração de embeddings de 512 dimensões utilizando FaceNet.
- Reconhecimento por similaridade de cosseno.
- Classificação de pessoas não reconhecidas como "Desconhecido".
- Armazenamento local criptografado.
- Listagem e exclusão de cadastros.

## Tecnologias

- Python
- Streamlit
- PyTorch
- facenet-pytorch
- MTCNN
- InceptionResnetV1 (FaceNet, pré-treinado com VGGFace2)
- NumPy
- Pillow
- SQLite
- Cryptography (Fernet)
- Keyring

## Estrutura do projeto

```text
FaceNet_App/
├── app.py
├── banco.py
├── reconhecimento.py
├── seguranca.py
├── autenticacao.py
├── configurar_senha.py
├── requirements.txt
├── .gitignore
├── README.md
└── docs/
    ├── specs/
    │   ├── 001-face-detection.md
    │   ├── 002-person-enrollment.md
    │   ├── 003-face-recognition.md
    │   ├── 004-unknown-person.md
    │   └── 005-camera-interface.md
    └── adr/
        ├── 001-facenet-model.md
        └── 002-data-storage-security.md
```

O diretório `dados_privados/` é criado localmente e não deve ser publicado no repositório.

## Instalação

Requisitos: Python compatível com as dependências do projeto e acesso ao terminal.

Clone o repositório e entre na pasta do aplicativo.

Crie um ambiente virtual:

```powershell
python -m venv .venv
```

Ative o ambiente no Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instale as dependências:

```powershell
python -m pip install -r requirements.txt
```

Configure uma senha de acesso:

```powershell
python configurar_senha.py
```

Execute o aplicativo:

```powershell
python -m streamlit run app.py --server.address 127.0.0.1
```

Abra o endereço:

`http://127.0.0.1:8501`

**Observação:** a primeira execução pode exigir o download dos pesos pré-treinados do FaceNet.

## Como utilizar

### Cadastrar uma pessoa

1. Faça login.
2. Acesse "Cadastrar pessoa".
3. Informe o nome e selecione uma fotografia ou utilize a câmera.
4. Confirme que existe autorização para o tratamento dos dados biométricos.
5. Realize o cadastro.

### Reconhecer uma pessoa

1. Acesse "Reconhecimento facial".
2. Envie uma fotografia ou utilize a câmera.
3. Clique em "Reconhecer rosto".
4. O aplicativo compara o embedding gerado com os cadastros existentes.

Se a maior similaridade atingir o limiar configurado, o sistema apresenta o nome correspondente. Caso contrário, informa que a pessoa é desconhecida.

## Avaliação e limitações

Na primeira parte do projeto, o FaceNet foi avaliado utilizando 6.000 pares faciais do conjunto LFW, obtendo acurácia média de 98,43% com similaridade de cosseno.

Esse resultado corresponde à avaliação experimental de verificação facial e não representa diretamente a acurácia do aplicativo.

O aplicativo utiliza atualmente um limiar provisório de 0,80. Os testes iniciais identificaram tanto um reconhecimento correto quanto uma falsa rejeição, indicando a necessidade de calibração adicional.

O sistema não implementa detecção de prova de vida e não deve ser utilizado como mecanismo único de autenticação em situações de alto risco.

## Privacidade e segurança

O projeto trata embeddings faciais como dados biométricos sensíveis.

As medidas implementadas incluem:

- Confirmação de consentimento antes do cadastro.
- Armazenamento local.
- Criptografia de nomes e embeddings com Fernet.
- Gerenciamento da chave criptográfica por meio do Keyring.
- Autenticação por senha.
- Exclusão de cadastros pela interface.
- Configuração `secure_delete` nas conexões SQLite.
- Exclusão do diretório `dados_privados/` do controle de versão.

A exclusão de um registro do banco não garante a remoção de todas as cópias ou vestígios externos.

O protótipo não representa, por si só, comprovação de conformidade integral com a LGPD.

**Nunca publique fotografias pessoais, embeddings biométricos, bancos de dados privados, chaves criptográficas ou senhas no GitHub.**

## Documentação

As especificações funcionais estão disponíveis em `docs/specs/`.

As decisões arquiteturais estão disponíveis em `docs/adr/`.

## Finalidade

Projeto desenvolvido exclusivamente para fins acadêmicos e experimentais, com utilização de imagens autorizadas.