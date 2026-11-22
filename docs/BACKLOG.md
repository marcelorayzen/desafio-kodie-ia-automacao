# Backlog — desafio-kodie-ia-automacao

Fila do que está em foco, na ordem. Ao fechar um item: resultado, commit, teste e evidência.

## Entregue na v1.0.0 (22/11/2026)

- [x] **1. Conferir o enunciado do desafio** — caso 4.1; exigências mapeadas em `PRODUCT.md`
  ("O que o enunciado exige"); origem dos valores no contrato.
- [x] **2. Testes verdes** — `pytest` num `.venv` limpo: 15 passed.
- [x] **3. Fixar um modelo estável do Gemini** — `gemini-3.5-flash` com `thinkingLevel: low` e
  `gemini-3.5-flash-lite` de reserva. Medição em `docs/ARQUITETURA.md`.
- [x] **4. Fluxo de ponta a ponta** — 4/4 setores na aba certa e a mensagem ambígua em
  `revisao_humana`. No caminho: `columns.schema` preenchido (exigido pelo n8n 2.x) e escala de
  confiança explícita no prompt (a ambígua tinha saído com 0,75; decisão: ajustar o prompt, não o
  limite).
- [x] **6. README nas 6 seções do enunciado** — ideia, problema, solução, tecnologias,
  funcionamento e como executar, incluindo Docker Compose.
- [x] **7. Prints do fluxo** — 20 prints em `docs/prints/`, descritos em `docs/FLUXO-N8N.md`:
  fluxo completo, cada nó, execução com sucesso, dados por etapa, planilha e caminho de erro.
- [x] **8. Entrega** — release `v1.0.0` sem deploy, com `CHANGELOG.md`; varredura do histórico
  sem segredos.

## Próximos

- [ ] **5. Conjunto de avaliação** (~20 mensagens fora dos exemplos do prompt, com categoria e
  setor esperados) — aceite: acerto medido e anotado. Incluir casos de fronteira, como "prazo de
  entrega" (`comercial` ou `atendimento`).
- [ ] Autenticação no webhook e na API, se o projeto for publicado.

## Fora deste marco

Canal real de mensagens, resposta automática ao cliente e painel próprio — o enunciado não pede.
