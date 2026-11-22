# Estado do projeto — desafio-kodie-ia-automacao

**Atualizado em:** 22/11/2026 · **Versão:** 1.0.0

Fotografia datada do projeto, não promessa.

## Como ler os estados

**Decidido** é escolha aprovada. **Implementado** é código no HEAD. **Testado** exige caso
executado com resultado conhecido. **Implantado** exige versão confirmada no ambiente.
**Em uso** exige ação real observada. Nenhum implica o seguinte.

## Fotografia

| área | estado | evidência e limite |
|---|---|---|
| API de classificação (`/classify`, `/health`) | Testado | `pytest`: **15 passed** em 22/11/2026, com IA falsa; inclui revisão humana, saída inválida, novas tentativas e modelo de reserva |
| Chamada real ao Gemini | Testado | `check_gemini.py` em 22/11/2026 com `gemini-3.5-flash` + `thinkingLevel: low`: 4/4 amostras corretas, inclusive a de injeção |
| Avaliação manual do prompt | Testado | 9/9 mensagens fora dos exemplos do prompt (`docs/QUALIDADE.md`); amostra pequena |
| Workflow do n8n | Testado | 22/11/2026, n8n 2.48.7: mensagens nas 5 abas certas, a ambígua em `revisao_humana` e uma pelo caminho de erro; prints em `docs/FLUXO-N8N.md` |
| Docker Compose | Testado | API saudável e n8n em `:5678`, subidos com `docker compose up -d` |
| Entrega exigida pelo enunciado | Implementado | README nas 6 seções, prints do fluxo, `workflow.json`, `.env.example`, Docker Compose |
| Publicação | Não implantado | roda só localmente, por decisão (ver abaixo) |

## Decisões ativas

- Entrega como GitHub Release `v1.0.0`, sem deploy (22/11/2026): o enunciado não pede serviço
  publicado, e publicar exigiria autenticação no webhook e na API.
- Para mensagens vagas, ajustar o prompt (escala de confiança explícita) em vez de mudar o limite
  de 0,6 (22/11/2026).
- ADR-0001 — Regra de classificação na API, não no n8n (`docs/decisions/`), status *Aceita* (22/11/2026).

## Próximos passos

Ver `docs/BACKLOG.md`: conjunto de avaliação maior (~20 mensagens) e autenticação, se o projeto
for publicado.
