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
| API de classificação (`/classify`, `/health`) | Testado | `pytest`: **15 passed** em 22/11/2026 (Python 3.14.4) — com IA falsa; inclui tentativas e modelo de reserva |
| Regras de revisão humana e reserva | Testado | baixa confiança e saída inválida cobertas pelos mesmos 10 testes |
| Chamada real ao Gemini | Testado | `check_gemini.py` em 22/11/2026 com `gemini-3.5-flash` + `thinkingLevel: low`: 4/4 amostras corretas (injeção → `outros`/`baixa`), sem 503, ~2 s cada |
| Workflow do n8n | Testado | 22/11/2026, n8n 2.48.7: webhook → API → Gemini → planilha; 4 mensagens de setor claro na aba certa e a ambígua em `revisao_humana` (confiança 0,3), conferido na planilha. Prints ainda não feitos |
| Docker Compose | Testado | subido em 22/11/2026: API saudável, `/classify` real 3/3 no container; n8n 2.48.7 em `:5678` |
| Documentação do padrão Rayzen | Implementado | AGENTS, PRODUCT, ARQUITETURA, CONTRATO, QUALIDADE, BACKLOG, ADR-0001 |
| Entrega exigida pelo enunciado | Parcial | faltam README nas 6 seções, prints do fluxo e repositório público (`PRODUCT.md`, "O que o enunciado exige") |
| Rayzen | Implantado | projeto `desafio-kodie-ia-automacao` registrado; hook resolve o repoSlug pela pasta |

## Decisões ativas

- ADR-0001 — Regra de classificação na API, não no n8n (`docs/decisions/`) — **Proposta**,
  registra o que o código já faz; aguarda o "sim" do Marcelo.

## Perguntas em aberto

Nenhuma no momento.

## Próxima missão

Item 7 (prints do fluxo, exigidos pelo enunciado) e item 6 (README nas 6 seções). Antes dos
prints, limpar as linhas de teste da planilha. Item 5 (conjunto de avaliação) já tem um começo:
9 mensagens na tabela de `docs/QUALIDADE.md`.
