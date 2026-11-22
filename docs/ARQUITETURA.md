# Arquitetura — desafio-kodie-ia-automacao

## Visão

Dois serviços pequenos, cada um fazendo o que faz melhor: a **API em Python** concentra a regra de
classificação (prompt, schema, validação, limite de confiança) e é testável sem IA; o **n8n** faz a
orquestração visível (receber, chamar, rotear, gravar). A regra não mora no n8n de propósito — ver
[ADR-0001](decisions/ADR-0001-classificacao-na-api.md).

```
cliente ─POST /webhook/mensagem─▶ n8n
                                   ├─ Normalizar entrada
                                   ├─ Classificar mensagem (API + IA) ─POST /classify─▶ API (FastAPI)
                                   │                                                     └─▶ Gemini (JSON com schema)
                                   ├─ erro na API ─▶ Preparar erro ─────────────┐
                                   └─ Rotear por setor                          ▼
                                        ├─ needs_human_review ─▶ Planilha: Revisão humana
                                        └─ atendimento | financeiro | suporte_tecnico | comercial
                                                              ─▶ Planilha: <setor>
```

## Módulos e responsabilidades

| módulo | responsabilidade | depende de |
|---|---|---|
| `app/main.py` | rotas `GET /health` e `POST /classify`; erro do provedor vira HTTP 502 | `classifier`, `config` |
| `app/classifier.py` | `GeminiClient` (chamada HTTP, timeout, erros sem vazar corpo) e `classify_message` (valida, aplica limite, reserva) | `prompt`, `schemas` |
| `app/prompt.py` | regras de classificação, exemplos e a mensagem delimitada (`<<< >>>`) | — |
| `app/schemas.py` | contrato de entrada e saída (valores permitidos) — também é o JSON Schema enviado ao Gemini | Pydantic |
| `app/config.py` | variáveis de ambiente | pydantic-settings |
| `scripts/build_workflow.py` | gera `n8n/workflow.json` | — |
| `n8n/workflow.json` | 10 nós: webhook → normalizar → classificar → rotear → 5 abas | API, Google Sheets |

## Dados, integrações e segurança

- **Persistência:** só a planilha do Google Sheets (via n8n). A API não guarda nada.
- **Integrações externas:** Gemini API (`generateContent`, `responseJsonSchema`) e Google Sheets
  (credencial selecionada no n8n; o JSON não a carrega).
- **Autenticação/autorização:** nenhuma na API nem no webhook — aceitável só rodando local
  (TODO(decisão): exigir token se for publicado).
- **Falhas:** Gemini fora, sem chave ou com HTTP ≠ 200 → `LLMError` → 502, e o n8n manda para a
  aba de revisão com o motivo. Resposta fora do schema → classificação de reserva com
  `needs_human_review=true`. Sem retentativa automática.
- **Observabilidade:** logs do uvicorn e as execuções do n8n; sem métricas.

## Tecnologias

| tecnologia | para quê | por que | alternativa considerada |
|---|---|---|---|
| FastAPI + Pydantic | API e contrato | o schema Pydantic vira o JSON Schema que o Gemini obedece | classificar direto no nó de IA do n8n |
| Gemini (`responseJsonSchema`) | classificar | saída estruturada no plano gratuito | OpenAI, que exige crédito |
| n8n | orquestração e planilha | é o tema do curso; fluxo visível | script Python agendado |
| Docker Compose | subir os dois juntos | o n8n só sobe com a API saudável (`healthcheck`) | rodar cada um à mão |

**Risco do modelo:** `GEMINI_MODEL=gemini-flash-latest` é um apelido que troca de versão sem aviso.
No Rayzen ele foi medido em 22/08/2026 com **200, 503, 503** em três chamadas seguidas e ficou de
fora por instável. Para a entrega, fixar um modelo estável e conferir com `check_gemini.py`.

## Deploy

Não publicado: roda local com `docker compose up -d`. Publicar pede autenticação no webhook e na
API antes (ver acima).
