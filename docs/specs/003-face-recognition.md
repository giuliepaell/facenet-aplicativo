# SPEC-003 — Reconhecimento Facial

## 1. Objetivo

Implementar o reconhecimento facial de pessoas previamente cadastradas, utilizando embeddings gerados pelo FaceNet e a similaridade de cosseno para comparar os rostos.

## 2. Tecnologias utilizadas

- **Python:** implementação da lógica de reconhecimento.
- **Streamlit:** interface do usuário.
- **MTCNN:** detecção e preparação facial.
- **FaceNet (InceptionResnetV1):** geração de embeddings de 512 dimensões.
- **NumPy:** operações matemáticas.
- **SQLite:** recuperação dos cadastros biométricos criptografados.

## 3. Requisitos funcionais

- **RF-001:** O sistema deve receber uma fotografia enviada ou capturada pela câmera.
- **RF-002:** O sistema deve verificar a presença de exatamente um rosto.
- **RF-003:** O sistema deve gerar um embedding facial de 512 dimensões.
- **RF-004:** O sistema deve recuperar os embeddings das pessoas cadastradas.
- **RF-005:** O sistema deve calcular a similaridade de cosseno entre o rosto consultado e os cadastros.
- **RF-006:** O sistema deve selecionar o cadastro com a maior similaridade.
- **RF-007:** O sistema deve reconhecer uma pessoa somente quando a similaridade atingir o limiar configurado.
- **RF-008:** O sistema deve informar quando a pessoa não puder ser reconhecida.

## 4. Fluxo de reconhecimento

1. O usuário autenticado acessa a página "Reconhecimento facial".
2. Envia uma imagem ou captura uma fotografia pela câmera.
3. O aplicativo utiliza o MTCNN para detectar o rosto.
4. O FaceNet gera um embedding de 512 dimensões.
5. O aplicativo recupera e descriptografa os embeddings cadastrados.
6. A similaridade de cosseno é calculada para cada cadastro.
7. O sistema identifica o cadastro com a maior similaridade.
8. Se a similaridade atingir o limiar configurado, o nome correspondente é apresentado.
9. Caso contrário, o resultado é "Desconhecido".

## 5. Similaridade de cosseno

A similaridade de cosseno mede a proximidade entre dois vetores considerando o ângulo formado entre eles.

Sua fórmula é:

**similaridade(A, B) = (A · B) / (||A|| × ||B||)**

Onde:

- **A:** embedding da imagem consultada.
- **B:** embedding de uma pessoa cadastrada.
- **A · B:** produto escalar entre os vetores.
- **||A|| e ||B||:** normas dos vetores.

Quanto maior a similaridade, maior a proximidade entre as representações faciais.

## 6. Limiar de reconhecimento

A implementação atual utiliza um limiar provisório de **0,80**.

A regra aplicada é:

- Similaridade maior ou igual a 0,80: o cadastro mais semelhante é aceito.
- Similaridade menor que 0,80: o resultado é "Desconhecido".

Esse limiar ainda não foi calibrado adequadamente para as imagens capturadas pela aplicação.

Na avaliação anterior com o conjunto LFW, foi encontrado um limiar de aproximadamente 0,40 para um procedimento específico de verificação de pares. Entretanto, esse valor não pode ser transferido automaticamente para o aplicativo, pois o processamento das imagens e a tarefa de identificação são diferentes.

## 7. Critérios de aceitação

- **CA-001:** O sistema deve gerar um embedding de 512 dimensões para uma imagem válida.
- **CA-002:** O sistema deve comparar o embedding consultado com os cadastros disponíveis.
- **CA-003:** O sistema deve selecionar a maior similaridade encontrada.
- **CA-004:** O sistema deve apresentar o nome quando a similaridade atingir o limiar.
- **CA-005:** O sistema deve apresentar "Desconhecido" quando a similaridade ficar abaixo do limiar.
- **CA-006:** O sistema deve tratar adequadamente a ausência de pessoas cadastradas.

## 8. Testes realizados

- Reconhecimento correto de uma pessoa cadastrada, com similaridade aproximada de **0,89**: **aprovado**.
- Fotografia diferente da mesma pessoa, com similaridade aproximada de **0,6369**, classificada como desconhecida: **falsa rejeição observada**.
- Fotografia de pessoa não cadastrada, com similaridade aproximada de **0,05**, classificada como desconhecida: **aprovado nesse teste**.
- Tentativa de reconhecimento sem cadastros disponíveis: **mensagem informativa apresentada**.

## 9. Limitações e melhorias futuras

- Calibrar o limiar de reconhecimento utilizando mais fotografias e participantes que tenham autorizado os testes.
- Avaliar taxas de falsa aceitação e falsa rejeição.
- Investigar variações de iluminação, posição do rosto e qualidade da câmera.
- Considerar mecanismos adicionais de proteção contra apresentação de fotografias à câmera.

## 10. Privacidade

O reconhecimento utiliza embeddings armazenados localmente e criptografados.

O sistema não deve disponibilizar embeddings, fotografias pessoais ou bancos de dados biométricos em repositórios públicos.

Os resultados devem ser utilizados somente para as finalidades autorizadas pelos participantes.