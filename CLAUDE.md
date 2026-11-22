# desafio-kodie-ia-automacao — Instruções para Claude Code

> Workflow pessoal e identidade no Rayzen em `CLAUDE.local.md` (fora do git).

## O que é

Desafio do curso Kodie (IA + automação): uma API que **classifica mensagens de clientes** com o
Gemini e um **workflow do n8n** que recebe a mensagem por webhook, chama a API e registra o resultado
numa planilha do Google Sheets.

**Dono:** Marcelo Rayzen
**Repositório:** `github.com/marcelorayzen/desafio-kodie-ia-automacao`
**Stack:** Python 3 · FastAPI · httpx · Pydantic · pytest · Gemini API · n8n · Docker Compose

## Estrutura

```
app/
  main.py         # FastAPI: GET /health, POST /classify
  classifier.py   # cliente Gemini (JSON com schema) + regra de classificação
  prompt.py       # prompt do sistema e montagem do prompt do usuário
  schemas.py      # modelos Pydantic de entrada e saída
  config.py       # variáveis de ambiente (pydantic-settings)
n8n/workflow.json         # webhook → API → Google Sheets
scripts/build_workflow.py # gera o workflow.json
scripts/check_gemini.py   # teste manual contra o Gemini real (usa o .env)
tests/test_api.py         # testes com cliente de IA falso
```

## Setup

```bash
python -m venv .venv && .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env      # preencher GEMINI_API_KEY e GOOGLE_SHEET_ID
pytest                    # testes (sem chamar o Gemini)
uvicorn app.main:app --reload --port 8000
docker compose up -d      # API em :8000 e n8n em :5678
```

## Regras

- **Nunca versionar o `.env`** — só o `.env.example`, com os campos secretos vazios.
- Os testes usam um cliente de IA falso; chamada real ao Gemini só em `scripts/check_gemini.py`.
- O texto da mensagem é de terceiro: o prompt (`app/prompt.py`) manda ignorar pedidos de dentro da
  mensagem para mudar regras ou formato, e `scripts/check_gemini.py` tem uma amostra de injeção
  ("Ignore as instruções anteriores…") para conferir contra o Gemini real.
- Resposta do modelo é validada pelo schema Pydantic; fora do formato, a API cai no caminho de
  reserva (`test_invalid_ai_output_falls_back`) — não inventa classificação. Confiança abaixo de
  `CONFIDENCE_THRESHOLD` marca a mensagem para revisão humana.
