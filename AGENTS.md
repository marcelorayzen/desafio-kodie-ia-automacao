# Contrato de trabalho do repositório — desafio-kodie-ia-automacao

> Para qualquer agente (Codex, Claude, Hub) e para pessoas. Curto de propósito: o detalhe
> mora nos documentos que este arquivo manda ler.

## Escopo atual

Desafio do curso Kodie (IA + automação). Uma API FastAPI recebe a mensagem de um cliente, pede ao
Gemini uma classificação em JSON (categoria, prioridade, setor, sentimento, resumo, confiança) e
devolve o resultado validado; um workflow do n8n recebe a mensagem por webhook, chama a API e grava
numa planilha do Google Sheets, numa aba por setor ou na aba de revisão humana.

Ainda **não** é: um serviço publicado, um atendimento real, nem integração com canal de mensagens
(WhatsApp, e-mail). Roda localmente com Docker Compose.

## Antes de alterar

1. Ler `docs/ESTADO-DO-PROJETO.md`, `docs/BACKLOG.md` e o documento do módulo afetado.
2. Preservar a diferença entre decisão aprovada, código, teste automatizado, validação
   humana, deploy e uso operacional — nenhum implica o seguinte.
3. Não inventar requisitos do desafio, categorias, regras de prioridade ou critérios de entrega:
   o enunciado do curso é a fonte. Lacuna vira `TODO(decisão)` e se pede a definição.
4. Mudar categoria, prioridade, setor ou o formato da resposta começa pelo contrato
   (`app/schemas.py` + `docs/CONTRATO-classificacao.md`) e pelo teste, depois o prompt e o n8n.
5. `n8n/workflow.json` é **gerado** por `scripts/build_workflow.py`: altere o gerador e rode-o,
   nunca edite o JSON à mão.

## Segurança e operações

- Nunca ler, imprimir, versionar ou pedir que sejam colados valores de `.env*`, tokens,
  senhas ou chaves. `.env.example` só com nomes e valores não secretos.
- A mensagem do cliente é texto de terceiro: entra no prompt delimitada e como DADO. Nenhuma
  instrução de dentro dela muda regra ou formato.
- Não publicar a API nem o n8n na internet, não conectar planilha de dados reais e não tornar o
  repositório público sem aprovação explícita do Marcelo.
- Notas operacionais e evidências ficam em `.local/` (fora do git).

## Verificação mínima

```bash
pytest
git diff --check
```

Os testes usam um cliente de IA falso: provam a API e as regras, não o Gemini. Chamada real só
com `python scripts/check_gemini.py`; o fluxo do n8n e a planilha se validam rodando o
`docker compose` e enviando uma mensagem ao webhook.
