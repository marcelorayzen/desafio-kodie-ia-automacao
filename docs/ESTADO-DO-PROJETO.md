# Estado do projeto — desafio-kodie-ia-automacao

**Atualizado em:** 22/11/2026 · **Modo:** Padrão

Este é o documento que o próximo agente lê primeiro. É fotografia datada, não promessa.

## Como ler os estados

**Decidido** é escolha aprovada. **Implementado** é código no HEAD. **Testado** exige caso
executado com resultado conhecido. **Implantado** exige versão confirmada no ambiente.
**Em uso** exige ação real observada. Nenhum implica o seguinte.

## Fotografia

| área | estado | evidência e limite |
|---|---|---|
| API de classificação (`/classify`, `/health`) | Testado | `pytest`: **10 passed** em 22/11/2026 (Python 3.14.4, `.venv` limpo) — com IA falsa; não prova o Gemini |
| Regras de revisão humana e reserva | Testado | baixa confiança e saída inválida cobertas pelos mesmos 10 testes |
| Chamada real ao Gemini | Implementado | `scripts/check_gemini.py` existe; nenhuma execução registrada aqui |
| Workflow do n8n | Implementado | `n8n/workflow.json` (10 nós, gerado por `scripts/build_workflow.py`); não importado/rodado |
| Docker Compose | Implementado | API com healthcheck e n8n dependente dela; não subido |
| Documentação do padrão Rayzen | Implementado | AGENTS, PRODUCT, ARQUITETURA, CONTRATO, QUALIDADE, BACKLOG, ADR-0001 |
| Entrega exigida pelo enunciado | Parcial | faltam README nas 6 seções, prints do fluxo e repositório público (`PRODUCT.md`, "O que o enunciado exige") |
| Rayzen | Implantado | projeto `desafio-kodie-ia-automacao` registrado; hook resolve o repoSlug pela pasta |

## Decisões ativas

- ADR-0001 — Regra de classificação na API, não no n8n (`docs/decisions/`) — **Proposta**,
  registra o que o código já faz; aguarda o "sim" do Marcelo.

## Perguntas em aberto

- TODO(decisão): qual modelo do Gemini fixar no lugar de `gemini-flash-latest`.

## Próxima missão

Item 3 do backlog — fixar o modelo do Gemini e rodar `check_gemini.py` (gasta cota) — e em
seguida o item 4, fluxo de ponta a ponta, que destrava os prints (item 7).
