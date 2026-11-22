# Backlog — desafio-kodie-ia-automacao

Fila do que está em foco, na ordem. Ao fechar um item: resultado, commit, teste e evidência.

## Próximos, em ordem

- [ ] **1. Conferir o enunciado do desafio** no PDF do curso e trazer para cá o que é exigido e
  como é avaliado — aceite: os `TODO(decisão)` de `PRODUCT.md` e do contrato respondidos.
- [x] **2. Testes verdes nesta máquina** — aceite: `pytest` passa num `.venv` limpo, com o
  resultado anotado no estado do projeto. **Feito em 22/11:** 10 passed (Python 3.14.4).
- [ ] **3. Fixar um modelo estável do Gemini** no lugar de `gemini-flash-latest` — aceite:
  `check_gemini.py` classifica as quatro amostras, inclusive a de injeção, sem 503.
- [ ] **4. Fluxo de ponta a ponta** — aceite: `docker compose up`, workflow importado, uma
  mensagem por setor e uma ambígua enviadas ao webhook chegam às abas certas da planilha.
- [ ] **5. Conjunto de avaliação** (~20 mensagens fora dos exemplos do prompt) — aceite: acerto de
  categoria e setor medido e anotado.

## Depois

- [ ] Autenticação no webhook e na API, se for publicar.
- [ ] Entrega do desafio (repositório público, vídeo ou o que o curso pedir).

## Fora deste marco

Canal real de mensagens, resposta automática ao cliente e painel próprio — não fazem parte do
desafio até onde se sabe (confirmar no item 1).
