# desafio-kodie-ia-automacao — guia para o Claude Code

> O contrato de trabalho é o [`AGENTS.md`](AGENTS.md) — leia primeiro; ele vale aqui também.
> Notas pessoais e operacionais: `CLAUDE.local.md` (fora do git).

## Contexto em uma frase

Desafio do curso Kodie: API em Python que classifica mensagens de clientes com o Gemini, e workflow
do n8n que recebe por webhook e grava no Google Sheets, por setor ou em revisão humana.

## Onde está cada coisa

| quer saber | onde |
|---|---|
| estado atual e o que vem | `docs/ESTADO-DO-PROJETO.md` · `docs/BACKLOG.md` |
| produto, problema e escopo | `PRODUCT.md` |
| arquitetura e decisões | `docs/ARQUITETURA.md` · `docs/decisions/` |
| categorias, prioridades, setores, revisão | `docs/CONTRATO-classificacao.md` |
| como se valida | `docs/QUALIDADE.md` |

## Comandos

```bash
python -m venv .venv && .venv\Scripts\activate && pip install -r requirements.txt
docker compose up -d                 # API :8000 e n8n :5678
pytest && git diff --check           # verificação mínima
python scripts/check_gemini.py       # Gemini real (gasta cota; usa o .env)
python scripts/build_workflow.py     # regenera n8n/workflow.json
```
