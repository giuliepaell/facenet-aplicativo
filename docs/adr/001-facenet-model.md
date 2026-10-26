# ADR-001 — Escolha do FaceNet para Reconhecimento Facial

**Status:** Aceito  
**Data:** 26/10/2026

## 1. Contexto

O projeto tem como objetivo desenvolver uma aplicação de reconhecimento facial capaz de cadastrar pessoas, detectar rostos e identificar indivíduos previamente cadastrados.

Para isso, é necessário utilizar um modelo de inteligência artificial que transforme imagens faciais em representações numéricas que possam ser comparadas.

Na primeira parte do projeto, foi realizada uma avaliação do FaceNet utilizando o conjunto de dados Labeled Faces in the Wild (LFW).

## 2. Decisão

Foi decidido utilizar o modelo **InceptionResnetV1**, disponibilizado pela biblioteca `facenet-pytorch`, com pesos pré-treinados no conjunto VGGFace2.

O modelo gera embeddings faciais de 512 dimensões.

A detecção e preparação dos rostos são realizadas pelo MTCNN, também disponibilizado pela biblioteca `facenet-pytorch`.

A comparação entre os embeddings é feita utilizando similaridade de cosseno.

## 3. Justificativa

A escolha foi baseada nos seguintes fatores:

- Disponibilidade de um modelo pré-treinado, evitando a necessidade de treinamento completo.
- Integração com Python e PyTorch.
- Possibilidade de execução local utilizando CPU.
- Geração de embeddings numéricos que podem ser comparados.
- Resultados obtidos na avaliação experimental realizada na primeira parte do projeto.

### Resultados da avaliação com LFW

Na avaliação de 6.000 pares faciais, distribuídos em 10 folds, foram registrados os seguintes resultados:

| Métrica | Resultado |
|---|---|
| Acurácia média com similaridade de cosseno | 98,43% |
| Desvio-padrão da acurácia | 0,69 ponto percentual |
| Precisão média | 98,79% |
| Recall médio | 98,07% |
| F1-score médio | 98,43% |
| FAR média | 1,20% |
| FRR média | 1,93% |

Esses resultados apoiaram a utilização do modelo como base para a aplicação.

Entretanto, as métricas de verificação facial no LFW não representam diretamente a taxa de acerto do aplicativo em condições reais.

## 4. Alternativas consideradas

### Treinar um modelo facial do zero

Não foi escolhido devido à necessidade de uma quantidade maior de dados, tempo de treinamento e recursos computacionais.

### Utilizar outro modelo de reconhecimento facial

Seria possível utilizar outras arquiteturas, como ArcFace, mas isso exigiria uma nova avaliação experimental e integração com a aplicação.

### Utilizar um serviço externo de reconhecimento facial

Não foi escolhido. A execução local oferece maior controle sobre o processamento dos dados biométricos e evita a necessidade de enviar imagens a uma API externa.

## 5. Consequências positivas

- Reutilização do modelo avaliado na primeira parte do trabalho.
- Integração direta com MTCNN e PyTorch.
- Execução local sem dependência de uma API de reconhecimento facial.
- Armazenamento de embeddings em vez de fotografias originais.
- Possibilidade de comparar novos rostos com pessoas cadastradas sem treinar novamente o modelo.

## 6. Limitações e consequências negativas

- O processamento na CPU pode ser mais lento.
- A qualidade do reconhecimento depende das condições da fotografia.
- O sistema pode apresentar falsas aceitações e falsas rejeições.
- O limiar de similaridade precisa ser calibrado para a aplicação.
- Os embeddings faciais continuam sendo dados biométricos sensíveis, mesmo sem o armazenamento das fotografias originais.
- O modelo não possui, por si só, mecanismos de detecção de prova de vida.

## 7. Resultado da decisão

O FaceNet foi integrado ao aplicativo Streamlit e utilizado com sucesso para gerar embeddings de 512 dimensões.

Nos testes iniciais, o aplicativo conseguiu reconhecer uma pessoa cadastrada e classificar uma pessoa não cadastrada como desconhecida.

Também foi observada uma falsa rejeição em outra fotografia da pessoa cadastrada, demonstrando a necessidade de novos testes e ajustes no limiar.

A decisão de utilizar o FaceNet permanece aceita, com a calibração do reconhecimento registrada como melhoria necessária.