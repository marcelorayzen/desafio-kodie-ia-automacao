# Changelog

Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/); versões seguem
[Semantic Versioning](https://semver.org/lang/pt-BR/).

## [1.0.0] — 2026-11-22

Primeira versão entregue do desafio **IA e Automação** (Kodie), caso 4.1 — Classificação de
Mensagens. Roda localmente com Docker Compose; não há serviço publicado.

### Adicionado

- API FastAPI com `POST /classify` e `GET /health`: classifica a mensagem em categoria,
  prioridade, setor, sentimento, resumo e confiança, com resposta em JSON validada por Pydantic.
- Integração com o Gemini (`gemini-3.5-flash`, raciocínio `low`) usando JSON Schema obrigatório
  na resposta.
- Revisão humana quando a confiança fica abaixo de 0,6, quando a IA responde fora do formato ou
  quando a IA está indisponível.
- Prompt estruturado com escala de confiança explícita, exemplos e a mensagem do cliente
  delimitada e tratada como dado (proteção contra instruções escondidas).
- Novas tentativas em erro passageiro do Gemini (429/5xx/timeout) e modelo de reserva
  (`gemini-3.5-flash-lite`).
- Workflow do n8n com 10 nós (webhook → normalização → API → roteamento → Google Sheets), com
  saída de erro que grava a mensagem na aba de revisão; gerado por `scripts/build_workflow.py`.
- Docker Compose com a API (com healthcheck) e o n8n 2.48.7.
- 15 testes automatizados com IA falsa e `scripts/check_gemini.py` para conferir o Gemini real.
- README nas seis seções pedidas pelo enunciado e documentação do fluxo com prints
  (`docs/FLUXO-N8N.md`).

### Limitações conhecidas

- Sem autenticação no webhook nem na API: uso local apenas.
- Depende da disponibilidade e da cota do Gemini; em instabilidade, uma classificação pode passar
  de 1 minuto.
- Avaliação do prompt feita com 9 mensagens (9/9 corretas): indica direção, não taxa de acerto.

[1.0.0]: https://github.com/marcelorayzen/desafio-kodie-ia-automacao/releases/tag/v1.0.0
