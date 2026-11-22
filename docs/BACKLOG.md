# Backlog — desafio-kodie-ia-automacao

Fila do que está em foco, na ordem. Ao fechar um item: resultado, commit, teste e evidência.

## Próximos, em ordem

- [x] **1. Conferir o enunciado do desafio** no PDF do curso — **Feito em 22/11:** caso 4.1;
  exigências mapeadas em `PRODUCT.md` ("O que o enunciado exige"); origem dos valores no contrato.
- [x] **2. Testes verdes nesta máquina** — aceite: `pytest` passa num `.venv` limpo, com o
  resultado anotado no estado do projeto. **Feito em 22/11:** 10 passed (Python 3.14.4).
- [x] **3. Fixar um modelo estável do Gemini** — **Feito em 22/11:** `gemini-3.5-flash` com
  `thinkingLevel: low`; `check_gemini.py` 4/4, sem 503. Medição em `docs/ARQUITETURA.md`.
- [x] **4. Fluxo de ponta a ponta** — **Feito em 22/11:** 4/4 setores na aba certa e a ambígua em
  `revisao_humana`, conferido na planilha. No caminho: `columns.schema` preenchido (exigido pelo
  n8n 2.x) e escala de confiança explícita no prompt (decisão do Marcelo: ajustar o prompt, não o
  limite — a ambígua tinha saído com 0,75).
- [ ] **5. Conjunto de avaliação** (~20 mensagens fora dos exemplos do prompt) — aceite: acerto de
  categoria e setor medido e anotado.

- [ ] **6. README nas 6 seções do enunciado** (ideia, problema, solução, tecnologias,
  funcionamento, como executar — incluindo Docker Compose) — aceite: cada seção presente e
  verdadeira em relação ao estado do projeto.
- [ ] **7. Prints do fluxo** (completo, execução com sucesso, cada node, dados por etapa), com
  descrição curta, em `docs/prints/` e referenciados no README — aceite: as quatro exigências da
  seção 7 do PDF cobertas. Depende do item 4.
- [ ] **8. Entrega** — repositório público e link enviado ao curso — aceite: aprovação explícita
  do Marcelo para tornar público, varredura sem segredo no histórico, link enviado.

## Depois

- [ ] Autenticação no webhook e na API, se for publicar.

## Fora deste marco

Canal real de mensagens, resposta automática ao cliente e painel próprio — o enunciado não pede
(confirmado no item 1). Vídeo também não é pedido.
