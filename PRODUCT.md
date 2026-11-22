# Produto — desafio-kodie-ia-automacao

## Problema

**Enunciado:** uma pequena empresa recebe mensagens de clientes misturadas — dúvida, reclamação,
pedido — e alguém precisa ler uma por uma para saber o que é urgente e para qual setor vai.
**Hoje:** triagem manual · **Deveria:** cada mensagem chega classificada e no lugar certo, e só o
que a IA não resolveu com confiança passa por uma pessoa.
**Quem sofre:** quem faz o atendimento · **Frequência/impacto:** `HIPÓTESE` — volume e custo da
triagem não medidos; é um cenário de desafio de curso.
**Evidência:** enunciado do desafio Kodie, caso **4.1 — Classificação de Mensagens** (PDF do
curso, não incluído no repositório; conferido em 22/11/2026).

## Para quem

| papel | o que precisa |
|---|---|
| atendimento | ver na planilha, por setor, o que chegou e o que é urgente |
| revisor humano | uma aba só com o que a IA não classificou com confiança, e o motivo |
| avaliador do curso | o fluxo funcionando de ponta a ponta e o código legível |

## Escopo

**Dentro:** classificar uma mensagem por vez (categoria, prioridade, setor, sentimento, resumo,
confiança); revisão humana abaixo do limite de confiança ou quando a IA responde fora do formato;
webhook do n8n → API → planilha por setor; rodar localmente com Docker Compose.
**Fora (de propósito):** canal real de mensagens (WhatsApp, e-mail), resposta automática ao
cliente, painel próprio, publicação na internet e dado real de cliente — nenhum é pedido pelo
enunciado ("não é necessário desenvolver uma interface visual completa").

## O que o enunciado exige

O desafio "não possui uma única resposta correta"; avalia pensamento crítico, prompts, integração
com API de IA, organização e validação de dados e fluxos de automação (seção 11 do PDF). Não há
nota ou rubrica numérica.

| exigência (seção do PDF) | onde está | situação em 22/11/2026 |
|---|---|---|
| API em FastAPI ou Express (5, 6) | `app/` (FastAPI) | Testado (15 testes) |
| integração com modelo de IA (6) | `app/classifier.py` + Gemini | Testado com o Gemini real |
| prompt estruturado (6) | `app/prompt.py` | Testado (avaliação manual 9/9) |
| resposta em JSON (6) | `app/schemas.py` | Testado |
| fluxo funcional no n8n ou Make + integração com a API (6) | `n8n/workflow.json` | Testado de ponta a ponta |
| README com 6 seções: ideia, problema, solução, tecnologias, funcionamento, como executar (8) | `README.md` | Feito |
| prints: fluxo completo, execução com sucesso, cada node configurado, dados por etapa, com descrição (7) | `docs/FLUXO-N8N.md` | Feito (20 prints) |
| JSON exportado do n8n (9) | `n8n/workflow.json` | Feito (importado e executado no n8n 2.48.7) |
| `.env.example` sem segredos (9) | `.env.example` | Feito |
| repositório público no GitHub e link enviado (6, 9) | GitHub | Release `v1.0.0` |
| opcional/diferencial: Dockerfile, `docker-compose.yml` com API e n8n, instruções no README (10) | raiz | Testado |

## Sucesso

| critério | como medir | cuidado (Goodhart) |
|---|---|---|
| a mensagem chega à aba do setor certo | mensagens de exemplo com setor esperado, rodadas pelo webhook | acertar só os exemplos do prompt não prova nada — usar mensagens que o prompt não traz |
| o incerto vai para revisão humana | mensagem ambígua termina na aba de revisão com motivo | baixar o limite de confiança "melhora" a automação mandando erro adiante |
| instrução escondida não muda a classificação | a amostra de injeção em `scripts/check_gemini.py` | testar só uma frase de injeção conhecida |

## Restrições e desconhecidos

- RESTRIÇÃO: desafio de curso, feito por uma pessoa; Gemini no plano gratuito (cota diária).
- RISCO: o modelo fixado (`gemini-3.5-flash`) pode ser desativado pelo Google, como o
  `gemini-2.5-flash` foi — sinal: HTTP 404 no `check_gemini.py`.
