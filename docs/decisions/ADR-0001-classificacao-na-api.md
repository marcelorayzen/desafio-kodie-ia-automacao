# ADR-0001 — Regra de classificação na API, não no n8n

**Status:** Proposta · **Data:** 22/11/2026
**Decidido por:** — (registra o que o código do commit inicial já faz; vira "Aceita" quando o
Marcelo confirmar)

## Contexto

O desafio junta IA e automação. O n8n tem nós de IA próprios e poderia classificar a mensagem
sozinho, com o prompt dentro do workflow.

## Opções consideradas

1. **Classificar no n8n** (nó de IA com o prompt) — prós: um serviço só, tudo visual · contras: o
   prompt e a validação ficam dentro de um JSON gerado, sem teste automatizado; a saída do modelo
   chega sem schema conferido.
2. **Classificar numa API Python chamada pelo n8n** — prós: o contrato (Pydantic) vira o JSON
   Schema que o Gemini obedece, a regra de revisão humana é testável com uma IA falsa, e o n8n fica
   só com a orquestração · contras: dois serviços para subir.

## Decisão

Opção 2: a API concentra prompt, schema, limite de confiança e reserva; o n8n recebe, chama, roteia
e grava.

## Por quê

A parte que erra é a IA. Com a regra na API, "o que acontece quando a IA responde errado" vira
teste (`test_invalid_ai_output_falls_back`, `test_low_confidence_flags_review`) em vez de
suposição.

## Consequências

Mais fácil: testar e mudar a regra sem abrir o n8n. Mais difícil: subir dois serviços — resolvido
pelo Docker Compose, que só sobe o n8n com a API saudável. Revisitar se o curso exigir a IA dentro
do n8n.

> ADRs não se reescrevem. Mudou de ideia → nova ADR, e esta passa a "Substituída por".
