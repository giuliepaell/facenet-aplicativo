# ADR-002 — Armazenamento Local e Segurança dos Dados Biométricos

**Status:** Aceito  
**Data:** 26/10/2026

## 1. Contexto

O aplicativo FaceNet precisa armazenar informações de pessoas cadastradas para realizar o reconhecimento facial.

Essas informações incluem nomes e embeddings faciais de 512 dimensões. Como os embeddings representam características biométricas, seu tratamento exige cuidados específicos de privacidade e segurança.

Foi necessário escolher uma solução de armazenamento que permitisse cadastrar, consultar e excluir registros, mantendo os dados protegidos e evitando sua publicação acidental.

## 2. Decisão

Foram escolhidas as seguintes tecnologias:

- **SQLite:** banco de dados local.
- **Fernet (biblioteca cryptography):** criptografia dos nomes e embeddings.
- **Keyring:** acesso ao gerenciador de credenciais do Windows.
- **PBKDF2-HMAC-SHA256:** derivação de hash para verificação da senha de acesso.
- **Gitignore:** exclusão dos arquivos privados do controle de versão.

O aplicativo é executado localmente e utiliza autenticação por senha para restringir o acesso à interface.

## 3. Justificativa

### 3.1 SQLite

O SQLite foi escolhido porque:

- Não exige a instalação de um servidor de banco de dados.
- É integrado ao Python por meio do módulo `sqlite3`.
- Permite armazenar, consultar e excluir cadastros.
- É adequado ao escopo de um protótipo acadêmico executado localmente.

O banco é armazenado em:

`dados_privados/cadastros.db`

### 3.2 Criptografia Fernet

O Fernet foi escolhido para proteger a confidencialidade dos nomes e embeddings armazenados.

Antes de salvar um cadastro, o aplicativo criptografa essas informações.

Quando precisa realizar o reconhecimento, o sistema recupera e descriptografa os embeddings para efetuar as comparações.

A criptografia protege os dados armazenados, mas não elimina os riscos associados ao acesso indevido ao computador, à aplicação ou à chave criptográfica.

### 3.3 Gerenciamento da chave

A chave Fernet é recuperada por meio da biblioteca `keyring`, utilizando o gerenciador de credenciais do Windows.

Essa abordagem evita manter a chave diretamente no código-fonte.

A implementação atual também possui um mecanismo de recuperação de chave a partir de arquivo local, quando disponível.

A perda da chave pode tornar os cadastros criptografados irrecuperáveis. Portanto, o gerenciamento e a recuperação segura da chave são pontos que precisam de atenção adicional.

### 3.4 Autenticação

A interface exige uma senha antes de permitir o acesso às funcionalidades.

A senha não é armazenada em texto puro: sua verificação utiliza PBKDF2-HMAC-SHA256, com salt e 600.000 iterações.

A autenticação protege o acesso pela interface, mas não substitui os mecanismos de segurança do sistema operacional nem o controle de acesso aos arquivos locais.

## 4. Estrutura dos dados

A tabela `pessoas` contém:

| Campo | Finalidade |
|---|---|
| `id` | Identificador do cadastro |
| `nome` | Nome armazenado de forma criptografada |
| `embedding` | Representação facial criptografada |
| `data_cadastro` | Data e hora do cadastro |

O aplicativo não foi projetado para armazenar permanentemente as fotografias originais utilizadas no cadastro.

## 5. Exclusão de cadastros

A interface permite excluir uma pessoa cadastrada.

A operação remove o registro da tabela `pessoas`, impedindo que ele continue sendo utilizado nas consultas normais do aplicativo.

Entretanto, a exclusão lógica no SQLite não garante, por si só, a eliminação irrecuperável de vestígios em páginas livres do banco, arquivos auxiliares ou cópias de segurança.

Será necessário validar a remoção diretamente no banco e avaliar medidas adicionais de descarte seguro dos dados.

## 6. Alternativas consideradas

### Banco de dados remoto

Não foi escolhido porque adicionaria dependências de infraestrutura, conexão e controles de segurança para transmissão e armazenamento remoto de dados biométricos.

### Armazenamento em arquivos sem criptografia

Não foi escolhido devido ao risco de exposição direta de nomes e embeddings.

### Armazenamento de fotografias originais

Não foi adotado como estratégia de cadastro. A aplicação utiliza embeddings para realizar as comparações faciais, reduzindo a quantidade de informações armazenadas, embora os embeddings continuem sendo dados biométricos sensíveis.

## 7. Consequências positivas

- Armazenamento local sem necessidade de servidor externo.
- Nomes e embeddings criptografados.
- Chave criptográfica separada do código-fonte.
- Autenticação para acessar a interface.
- Possibilidade de consultar e excluir cadastros.
- Diretório `dados_privados/` incluído no `.gitignore`.

## 8. Limitações e riscos

- A segurança depende também da proteção do computador e das credenciais do Windows.
- A perda da chave criptográfica pode impedir a recuperação dos registros.
- O aplicativo ainda não possui limitação de tentativas de login.
- A exclusão precisa de validação adicional.
- O consentimento é confirmado na interface, mas a implementação atual não mantém um registro separado e auditável dessa autorização.
- A conformidade integral com a LGPD depende também de procedimentos organizacionais, finalidade, transparência, retenção e atendimento aos direitos dos titulares.

## 9. Resultado da decisão

O armazenamento local com SQLite e criptografia Fernet foi implementado.

Foram realizados testes de cadastro, recuperação de informações criptografadas, autenticação e exclusão pela interface.

A decisão permanece aceita para o protótipo acadêmico, com melhorias de segurança e validação da exclusão identificadas para as próximas etapas.