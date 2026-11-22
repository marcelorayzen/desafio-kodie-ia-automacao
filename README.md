# desafio-kodie-ia-automacao

Classificador de mensagens de clientes com IA: uma API que pede ao Gemini categoria, prioridade,
setor e sentimento de cada mensagem, e um workflow do n8n que registra o resultado no Google Sheets,
separado por setor, mandando para revisão humana o que a IA não classificou com confiança.

**Estado:** Padrão · protótipo (desafio do curso Kodie) — ver
[`docs/ESTADO-DO-PROJETO.md`](docs/ESTADO-DO-PROJETO.md).

## Como rodar

```bash
python -m venv .venv && .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # preencher GEMINI_API_KEY e GOOGLE_SHEET_ID
pytest                          # testes, sem chamar o Gemini
docker compose up -d            # API em http://localhost:8000 e n8n em http://localhost:5678
```

No n8n: importar `n8n/workflow.json` e selecionar a credencial do Google Sheets (o JSON não leva
credencial nenhuma).

```bash
curl -X POST http://localhost:8000/classify -H "Content-Type: application/json" \
  -d '{"message": "Preciso da segunda via do boleto de março."}'
```

## Documentação

| documento | responde |
|---|---|
| [`AGENTS.md`](AGENTS.md) | como trabalhar neste repositório (pessoas e agentes) |
| [`PRODUCT.md`](PRODUCT.md) | problema, para quem, escopo |
| [`docs/ARQUITETURA.md`](docs/ARQUITETURA.md) | como está construído e por quê |
| [`docs/CONTRATO-classificacao.md`](docs/CONTRATO-classificacao.md) | categorias, prioridades, setores e quando vai para revisão |
| [`docs/QUALIDADE.md`](docs/QUALIDADE.md) | como se valida |
