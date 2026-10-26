# SPEC-004 — Tratamento de Pessoas Desconhecidas

## 1. Objetivo

Permitir que o aplicativo identifique situações em que um rosto não corresponde, com confiança suficiente, a nenhuma pessoa cadastrada, evitando atribuições automáticas de identidade sem atingir o limiar de similaridade estabelecido.

## 2. Tecnologias utilizadas

- **Python:** implementação das regras de decisão.
- **FaceNet:** geração dos embeddings faciais.
- **NumPy:** cálculo da similaridade de cosseno.
- **Streamlit:** apresentação dos resultados.
- **SQLite:** consulta aos cadastros existentes.

## 3. Requisitos funcionais

- **RF-001:** O sistema deve comparar o rosto consultado com os embeddings cadastrados.
- **RF-002:** O sistema deve selecionar a maior similaridade encontrada.
- **RF-003:** O sistema deve classificar como "Desconhecido" um rosto cuja maior similaridade seja inferior ao limiar configurado.
- **RF-004:** O sistema deve informar quando não existirem pessoas cadastradas.
- **RF-005:** O sistema não deve cadastrar automaticamente pessoas desconhecidas.
- **RF-006:** O sistema deve impedir o reconhecimento quando não houver exatamente um rosto válido na imagem.

## 4. Fluxo de funcionamento

1. O usuário autenticado fornece uma imagem para reconhecimento.
2. O MTCNN detecta o rosto.
3. O FaceNet gera um embedding de 512 dimensões.
4. O aplicativo recupera os embeddings cadastrados.
5. O sistema calcula a similaridade de cosseno entre o rosto consultado e cada cadastro.
6. O maior valor de similaridade é selecionado.
7. Se esse valor for inferior ao limiar, o resultado será "Desconhecido".
8. Se não houver cadastros, o aplicativo informa que não existem pessoas disponíveis para comparação.

## 5. Regra de decisão

A implementação atual utiliza um limiar provisório de **0,80**.

- **Similaridade ≥ 0,80:** o cadastro mais semelhante é reconhecido.
- **Similaridade menor que 0,80:** o rosto é classificado como desconhecido.
- **Banco de dados vazio:** não é possível identificar uma pessoa cadastrada.

O limiar ainda precisa ser calibrado com mais testes.

A classificação "Desconhecido" não significa necessariamente que a pessoa nunca tenha sido cadastrada. Também pode ocorrer uma falsa rejeição causada por diferenças de iluminação, ângulo, qualidade da imagem ou outras condições.

## 6. Critérios de aceitação

- **CA-001:** Uma pessoa não cadastrada, com similaridade abaixo do limiar, deve ser classificada como desconhecida.
- **CA-002:** Uma pessoa cadastrada pode ser reconhecida quando sua similaridade atingir o limiar.
- **CA-003:** O aplicativo deve tratar corretamente um banco de dados sem cadastros.
- **CA-004:** O reconhecimento não deve criar novos registros biométricos.
- **CA-005:** O aplicativo deve informar quando não for possível processar um rosto válido.

## 7. Testes realizados

- Pessoa não cadastrada, com similaridade aproximada de **0,05**: classificada como desconhecida.
- Pessoa cadastrada, com similaridade aproximada de **0,89**: reconhecida corretamente.
- Outra fotografia da mesma pessoa cadastrada, com similaridade aproximada de **0,6369**: classificada como desconhecida, caracterizando uma falsa rejeição.
- Reconhecimento com banco de dados vazio: mensagem informativa apresentada.

Esses testes demonstram o funcionamento básico da regra de decisão, mas não são suficientes para estimar a precisão geral do sistema.

## 8. Privacidade e segurança

O aplicativo não realiza cadastro automático de rostos desconhecidos.

As imagens utilizadas para reconhecimento não são armazenadas permanentemente pela implementação atual.

Os embeddings cadastrados permanecem criptografados no banco de dados local e são recuperados para comparação durante a operação.

## 9. Limitações e melhorias futuras

- Calibrar o limiar com um conjunto maior de fotografias autorizadas.
- Avaliar a taxa de falsa aceitação (FAR).
- Avaliar a taxa de falsa rejeição (FRR).
- Testar diferentes condições de iluminação, distância e posicionamento.
- Evitar apresentar o resultado como identificação definitiva em aplicações sensíveis.