# SPEC-005 — Interface de Captura pela Câmera

## 1. Objetivo

Permitir que o usuário capture fotografias diretamente pela câmera do dispositivo para realizar cadastros e reconhecimento facial, sem depender exclusivamente de imagens armazenadas no computador.

## 2. Tecnologias utilizadas

- **Python:** linguagem de programação.
- **Streamlit:** interface gráfica e captura de fotografias.
- **Pillow:** abertura e conversão das imagens.
- **MTCNN:** detecção facial.
- **FaceNet:** geração dos embeddings faciais.

## 3. Requisitos funcionais

- **RF-001:** O sistema deve permitir capturar uma fotografia pela câmera.
- **RF-002:** O sistema deve permitir enviar uma imagem existente como alternativa à câmera.
- **RF-003:** O sistema deve disponibilizar a câmera na página de cadastro.
- **RF-004:** O sistema deve disponibilizar a câmera na página de reconhecimento.
- **RF-005:** O sistema deve apresentar uma prévia da fotografia selecionada.
- **RF-006:** O sistema deve converter a imagem para RGB antes do processamento.
- **RF-007:** O sistema deve permitir processar a fotografia capturada utilizando MTCNN e FaceNet.

## 4. Implementação

A captura de fotografias é realizada pelo componente `st.camera_input()` do Streamlit.

Exemplo utilizado no cadastro:

```python
foto_camera = st.camera_input(
    "Ou tire uma fotografia com a câmera",
    key="camera_cadastro"
)
```

A imagem capturada é priorizada quando o usuário também seleciona um arquivo:

```python
foto_escolhida = foto_camera if foto_camera is not None else foto
```

A imagem é convertida para RGB utilizando Pillow:

```python
imagem_cadastro = Image.open(foto_escolhida).convert("RGB")
```

A mesma estratégia é utilizada na página de reconhecimento facial, com identificadores diferentes para os componentes.

## 5. Fluxo de funcionamento

1. O usuário autenticado acessa a página de cadastro ou reconhecimento.
2. Escolhe entre enviar uma fotografia ou utilizar a câmera.
3. Caso escolha a câmera, autoriza seu uso no navegador.
4. Captura uma fotografia.
5. O aplicativo apresenta a imagem selecionada.
6. O usuário inicia o cadastro ou o reconhecimento.
7. O MTCNN detecta e prepara o rosto.
8. O FaceNet gera o embedding utilizado na operação.

## 6. Critérios de aceitação

- **CA-001:** A câmera deve permitir capturar uma fotografia quando o dispositivo e o navegador oferecem suporte.
- **CA-002:** A fotografia capturada deve ser exibida na interface.
- **CA-003:** O sistema deve permitir utilizar arquivos JPG, JPEG e PNG como alternativa.
- **CA-004:** A fotografia capturada deve poder ser utilizada no cadastro facial.
- **CA-005:** A fotografia capturada deve poder ser utilizada no reconhecimento facial.
- **CA-006:** O aplicativo deve continuar disponível quando o usuário optar por não utilizar a câmera.

## 7. Testes realizados

- Captura de fotografia pela câmera na página de cadastro: **aprovado**.
- Captura de fotografia pela câmera na página de reconhecimento: **aprovado**.
- Exibição da imagem selecionada: **aprovado**.
- Processamento facial após a captura: **aprovado**.
- Testes em diferentes navegadores e dispositivos: **pendentes**.
- Teste de permissão de câmera negada: **pendente**.

## 8. Privacidade

O acesso à câmera depende da autorização do usuário no navegador.

A aplicação utiliza fotografias para executar as operações solicitadas, sem implementar armazenamento permanente das imagens originais.

O cadastro de dados biométricos exige consentimento específico, conforme a especificação SPEC-002.

O aplicativo foi configurado para execução local, utilizando o endereço `127.0.0.1`.

## 9. Limitações

- A câmera depende das permissões e da compatibilidade do navegador.
- A captura é realizada por fotografias individuais, não por reconhecimento contínuo em vídeo.
- A qualidade da iluminação e da câmera pode afetar a detecção e o reconhecimento.
- A implementação atual não possui mecanismo de detecção de prova de vida.