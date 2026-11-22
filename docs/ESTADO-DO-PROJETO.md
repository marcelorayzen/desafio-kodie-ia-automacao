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
| API de classificação (`/classify`, `/health`) | Implementado | código no commit inicial `b6c8de7`; testes escritos em `tests/test_api.py` — **ainda não executados nesta máquina** |
| Regras de revisão humana e reserva | Implementado | `classify_message` + testes de baixa confiança e saída inválida, idem |
| Chamada real ao Gemini | Implementado | `scripts/check_gemini.py` existe; nenhuma execução registrada aqui |
| Workflow do n8n | Implementado | `n8n/workflow.json` (10 nós, gerado por `scripts/build_workflow.py`); não importado/rodado |
| Docker Compose | Implementado | API com healthcheck e n8n dependente dela; não subido |
| Documentação do padrão Rayzen | Implementado | AGENTS, PRODUCT, ARQUITETURA, CONTRATO, QUALIDADE, BACKLOG, ADR-0001 |
| Rayzen | Implantado | projeto `desafio-kodie-ia-automacao` registrado; hook resolve o repoSlug pela pasta |

## Decisões ativas

- ADR-0001 — Regra de classificação na API, não no n8n (`docs/decisions/`) — **Proposta**,
  registra o que o código já faz; aguarda o "sim" do Marcelo.

## Perguntas em aberto

- TODO(decisão): enunciado e critério de avaliação do desafio (estão no PDF do curso).
- TODO(decisão): os valores de categoria, prioridade e setor vieram do enunciado ou foram escolhidos?
- TODO(decisão): qual modelo do Gemini fixar no lugar de `gemini-flash-latest`.

## Próxima missão

Itens 1 e 2 do backlog — **aceite:** enunciado conferido e `pytest` verde num `.venv` limpo.
