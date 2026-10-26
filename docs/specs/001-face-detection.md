# SPEC-001 — Detecção Facial

## 1. Objetivo

Implementar a detecção automática de rostos em fotografias enviadas pelo usuário ou capturadas pela câmera, utilizando o algoritmo MTCNN.

## 2. Tecnologias utilizadas

- **Python:** linguagem de programação.
- **Streamlit:** interface do aplicativo.
- **MTCNN (facenet-pytorch):** detecção e preparação dos rostos.
- **Pillow:** manipulação das imagens.

## 3. Requisitos funcionais

- **RF-001:** O sistema deve permitir o envio de imagens nos formatos JPG, JPEG e PNG.
- **RF-002:** O sistema deve permitir capturar fotografias pela câmera.
- **RF-003:** O sistema deve detectar rostos presentes na imagem.
- **RF-004:** O sistema deve exibir retângulos ao redor dos rostos detectados.
- **RF-005:** O sistema deve informar quando nenhum rosto for encontrado.
- **RF-006:** O sistema deve permitir gerar um embedding para reconhecimento somente quando houver exatamente um rosto.

## 4. Fluxo de funcionamento

1. O usuário envia uma fotografia ou utiliza a câmera.
2. O aplicativo converte a imagem para RGB.
3. O MTCNN analisa a imagem e identifica os rostos.
4. O aplicativo desenha retângulos ao redor dos rostos encontrados.
5. Caso exista exatamente um rosto, ele poderá ser preparado para o FaceNet.
6. Caso não exista nenhum rosto ou existam múltiplos rostos, o reconhecimento não prossegue.

## 5. Configuração do MTCNN

```python
mtcnn = MTCNN(
    image_size=160,
    margin=0,
    keep_all=False,
    device="cpu"
)
```

O MTCNN prepara o rosto com dimensões de 160 × 160 pixels, sem margem adicional, utilizando a CPU.

## 6. Critérios de aceitação

- **CA-001:** Uma fotografia com um rosto deve permitir a detecção facial.
- **CA-002:** Uma fotografia sem rostos deve apresentar uma mensagem