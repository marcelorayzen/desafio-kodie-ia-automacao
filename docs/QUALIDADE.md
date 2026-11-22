# Qualidade — desafio-kodie-ia-automacao

## Verificação mínima (todo commit)

`pytest` e `git diff --check` — o mesmo que o `AGENTS.md` exige.

## Estratégia de teste

| nível | o que cobre | ferramenta |
|---|---|---|
| unitário/API | `/health`, classificação válida, revisão por baixa confiança, saída inválida da IA → reserva, falha do provedor → 502, validação da entrada | pytest + cliente de IA falso (`tests/test_api.py`) |
| IA real | as quatro amostras, inclusive a de injeção | `python scripts/check_gemini.py` (manual, gasta cota) |
| ponta a ponta | webhook → API → aba certa da planilha, e erro → aba de revisão | n8n rodando + `curl` no webhook (manual) |

## Critérios de aceite por entrega

- Mudança no contrato (`docs/CONTRATO-classificacao.md`) coberta por teste com o cliente falso.
- Defeito corrigido ganha teste que falhava antes.
- Mudança no prompt conferida com `check_gemini.py`, inclusive a amostra de injeção.

## Avaliação de IA

Ainda não há conjunto fixo de mensagens com resposta esperada. TODO(decisão): montar ~20 mensagens
que **não** estão nos exemplos do prompt, com categoria e setor esperados, e medir o acerto — sem
isso, "classifica bem" é impressão.

## O que os testes NÃO provam

Os testes de `pytest` não chamam o Gemini nem o n8n: provam a API e as regras com uma IA falsa.
Que o Gemini classifica bem, que o fluxo do n8n roda e que a planilha recebe as linhas só se prova
rodando de verdade.
