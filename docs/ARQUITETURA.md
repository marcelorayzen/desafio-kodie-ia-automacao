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

**Modelo:** `gemini-3.5-flash` (versão `3.5-flash-05-2026`) com `thinkingLevel: low`, fixado em
22/11/2026. Antes era `gemini-flash-latest`, apelido que troca de versão sem aviso (medido no
Rayzen em 22/08/2026 com 200, 503, 503). Medição de 22/11, mesma mensagem de cobrança dupla:

| modelo | raciocínio | tempo | resultado |
|---|---|---|---|
| `gemini-3.7-flash` | padrão | ~65 s/msg | 4 amostras certas — lento demais para o n8n |
| `gemini-3.7-flash` | `low` | 85 s | certo; `minimal` não é aceito (HTTP 400) |
| `gemini-3.5-flash` | `low` | 1,7 s | certo — **escolhido** |
| `gemini-3.5-flash-lite` | padrão | 1,2 s | certo — reserva, se a cota apertar |
| `gemini-2.5-flash` | — | — | HTTP 404 (desativado) |

**Instabilidade (22/11, à tarde):** o `gemini-3.5-flash` alternou sucesso, 503 e timeout; o
`flash-lite` também deu 503 pontual. Por isso o cliente tenta **2 vezes por modelo** em erro
passageiro (429/5xx/timeout, espera de 1,5 s) e depois passa para `GEMINI_FALLBACK_MODEL`; 404
pula direto para a reserva; 400/401/403 falham na hora. Pior caso ~2 min — o nó HTTP do n8n
espera 150 s. Medido no container: 3/3 classificações certas, em 4 s, 68 s e 63 s.

## Deploy

Não publicado: roda local com `docker compose up -d`. Publicar pede autenticação no webhook e na
API antes (ver acima).
