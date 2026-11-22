# Produto — desafio-kodie-ia-automacao

## Problema

**Enunciado:** uma pequena empresa recebe mensagens de clientes misturadas — dúvida, reclamação,
pedido — e alguém precisa ler uma por uma para saber o que é urgente e para qual setor vai.
**Hoje:** triagem manual · **Deveria:** cada mensagem chega classificada e no lugar certo, e só o
que a IA não resolveu com confiança passa por uma pessoa.
**Quem sofre:** quem faz o atendimento · **Frequência/impacto:** `HIPÓTESE` — volume e custo da
triagem não medidos; é um cenário de desafio de curso.
**Evidência:** TODO(decisão): o enunciado do desafio do curso Kodie (está no PDF do curso).

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
desafio até onde se sabe (TODO(decisão): confirmar no enunciado).

## Sucesso

| critério | como medir | cuidado (Goodhart) |
|---|---|---|
| a mensagem chega à aba do setor certo | mensagens de exemplo com setor esperado, rodadas pelo webhook | acertar só os exemplos do prompt não prova nada — usar mensagens que o prompt não traz |
| o incerto vai para revisão humana | mensagem ambígua termina na aba de revisão com motivo | baixar o limite de confiança "melhora" a automação mandando erro adiante |
| instrução escondida não muda a classificação | a amostra de injeção em `scripts/check_gemini.py` | testar só uma frase de injeção conhecida |

## Restrições e desconhecidos

- RESTRIÇÃO: desafio de curso, feito por uma pessoa; Gemini no plano gratuito (cota diária).
- DESCONHECIDO: o enunciado exato e o critério de avaliação do curso — impacto: decide o que
  falta entregar. Fonte: o PDF do curso.
- DESCONHECIDO: o modelo `gemini-flash-latest` é um apelido que muda de versão — impacto: a
  classificação pode mudar sem mudança no código.
