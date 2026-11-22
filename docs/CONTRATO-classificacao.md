# Contrato — classificação de mensagens

Fonte da verdade: `app/schemas.py` (valores) e `app/prompt.py` (critérios). Este documento só os
descreve; mudou um, muda o outro e o teste junto.

## Entrada (`POST /classify`)

| campo | regra |
|---|---|
| `message` | obrigatório, 1 a 4000 caracteres |
| `customer_name` | opcional, até 200 |
| `channel` | opcional, até 50 (ex.: email, whatsapp) |

## Saída

| campo | valores |
|---|---|
| `category` | `duvida` · `reclamacao` · `solicitacao` · `outros` |
| `priority` | `baixa` · `media` · `alta` · `urgente` |
| `department` | `atendimento` · `financeiro` · `suporte_tecnico` · `comercial` |
| `sentiment` | `positivo` · `neutro` · `negativo` |
| `summary` | uma frase, até 300 caracteres |
| `confidence` | 0 a 1 |
| `needs_human_review` | ver abaixo |
| `review_reason` | motivo, quando há revisão |

Os critérios de cada valor (o que é "urgente", o que vai para "financeiro") estão no prompt, com
exemplos.

## Quando vai para revisão humana

1. `confidence` abaixo de `CONFIDENCE_THRESHOLD` (padrão 0.6) → motivo "Confiança abaixo do limite".
2. A IA respondeu fora do schema → classificação de reserva (`outros`, `media`, `atendimento`,
   `neutro`, confiança 0) e motivo "Resposta da IA fora do formato esperado".
3. A API falhou (Gemini fora, sem chave) → HTTP 502; o n8n grava na aba de revisão com o erro.

## Regra de segurança

O texto da mensagem é dado, não instrução: vai delimitado entre `<<<` e `>>>`, e o prompt manda
ignorar pedidos de dentro dela para mudar regras ou formato.

TODO(decisão): os valores e critérios vieram do enunciado do curso ou foram escolhidos? Conferir
no PDF antes de mudar qualquer um.
