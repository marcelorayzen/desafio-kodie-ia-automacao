"""Gera n8n/workflow.json. Rode: python scripts/build_workflow.py

Mantemos o gerador no repositório para o fluxo ser reproduzível e revisável.
O JSON exportado não contém credenciais: o n8n pede para você selecionar a sua.
"""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "n8n" / "workflow.json"

SHEET_ID_EXPR = "={{ $env.GOOGLE_SHEET_ID }}"
SRC = "$('Normalizar entrada').item.json"

COLUMNS = {
    "data_hora": "={{ $now.format('yyyy-MM-dd HH:mm:ss') }}",
    "cliente": f"={{{{ {SRC}.customer_name }}}}",
    "canal": f"={{{{ {SRC}.channel }}}}",
    "mensagem": f"={{{{ {SRC}.message }}}}",
    "categoria": "={{ $json.category }}",
    "prioridade": "={{ $json.priority }}",
    "setor": "={{ $json.department }}",
    "sentimento": "={{ $json.sentiment }}",
    "resumo": "={{ $json.summary }}",
    "confianca": "={{ $json.confidence }}",
    "revisao_humana": "={{ $json.needs_human_review }}",
    "motivo_revisao": "={{ $json.review_reason }}",
}


def sheets_node(name, tab, position):
    return {
        "parameters": {
            "operation": "append",
            "documentId": {"__rl": True, "value": SHEET_ID_EXPR, "mode": "id"},
            "sheetName": {"__rl": True, "value": tab, "mode": "name"},
            "columns": {
                "mappingMode": "defineBelow",
                "value": COLUMNS,
                "matchingColumns": [],
                "schema": [],
            },
            "options": {},
        },
        "name": name,
        "type": "n8n-nodes-base.googleSheets",
        "typeVersion": 4.5,
        "position": position,
        "credentials": {"googleSheetsOAuth2Api": {"id": "", "name": "Google Sheets account"}},
    }


def assign(id_, name, value, type_="string"):
    return {"id": id_, "name": name, "value": value, "type": type_}


def rule(key, left, op, right=None):
    operator = {"type": "string", "operation": "equals"}
    cond = {"id": f"c-{key}", "leftValue": left, "operator": operator}
    if right is not None:
        cond["rightValue"] = right
    return {
        "conditions": {
            "options": {"caseSensitive": True, "leftValue": "", "typeValidation": "strict", "version": 2},
            "conditions": [cond],
            "combinator": "and",
        },
        "renameOutput": True,
        "outputKey": key,
    }


review_rule = {
    "conditions": {
        "options": {"caseSensitive": True, "leftValue": "", "typeValidation": "strict", "version": 2},
        "conditions": [
            {
                "id": "c-review",
                "leftValue": "={{ $json.needs_human_review }}",
                "operator": {"type": "boolean", "operation": "true", "singleValue": True},
            }
        ],
        "combinator": "and",
    },
    "renameOutput": True,
    "outputKey": "Revisão humana",
}

DEPARTMENTS = ["atendimento", "financeiro", "suporte_tecnico", "comercial"]

nodes = [
    {
        "parameters": {
            "httpMethod": "POST",
            "path": "mensagem",
            "responseMode": "lastNode",
            "options": {},
        },
        "name": "Webhook",
        "type": "n8n-nodes-base.webhook",
        "typeVersion": 2,
        "position": [0, 300],
        "webhookId": "5b0d6f0e-6b1e-4c53-9d5e-0c1b6f2a7e11",
    },
    {
        "parameters": {
            "assignments": {
                "assignments": [
                    assign("a1", "message", "={{ $json.body.message }}"),
                    assign("a2", "customer_name", "={{ $json.body.customer_name ?? '' }}"),
                    assign("a3", "channel", "={{ $json.body.channel ?? 'webhook' }}"),
                ]
            },
            "options": {},
        },
        "name": "Normalizar entrada",
        "type": "n8n-nodes-base.set",
        "typeVersion": 3.4,
        "position": [220, 300],
    },
    {
        "parameters": {
            "method": "POST",
            "url": "http://api:8000/classify",
            "sendBody": True,
            "specifyBody": "json",
            "jsonBody": "={{ JSON.stringify({ message: $json.message, customer_name: $json.customer_name || null, channel: $json.channel }) }}",
            "options": {"timeout": 60000},
        },
        "name": "Classificar mensagem (API + IA)",
        "type": "n8n-nodes-base.httpRequest",
        "typeVersion": 4.2,
        "position": [440, 300],
        "onError": "continueErrorOutput",
    },
    {
        "parameters": {
            "assignments": {
                "assignments": [
                    assign("e1", "category", "outros"),
                    assign("e2", "priority", "media"),
                    assign("e3", "department", "atendimento"),
                    assign("e4", "sentiment", "neutro"),
                    assign("e5", "summary", "Falha ao classificar a mensagem."),
                    assign("e6", "confidence", 0, "number"),
                    assign("e7", "needs_human_review", True, "boolean"),
                    assign("e8", "review_reason", "={{ 'Erro na API de classificação: ' + ($json.error?.message ?? 'desconhecido') }}"),
                ]
            },
            "options": {},
        },
        "name": "Preparar erro",
        "type": "n8n-nodes-base.set",
        "typeVersion": 3.4,
        "position": [700, 560],
    },
    {
        "parameters": {
            "rules": {
                "values": [review_rule]
                + [rule(d, "={{ $json.department }}", "equals", d) for d in DEPARTMENTS]
            },
            "options": {},
        },
        "name": "Rotear por setor",
        "type": "n8n-nodes-base.switch",
        "typeVersion": 3.2,
        "position": [700, 260],
    },
    sheets_node("Planilha: Revisão humana", "revisao_humana", [1000, 0]),
]

for i, d in enumerate(DEPARTMENTS):
    nodes.append(sheets_node(f"Planilha: {d}", d, [1000, 180 + i * 180]))

connections = {
    "Webhook": {"main": [[{"node": "Normalizar entrada", "type": "main", "index": 0}]]},
    "Normalizar entrada": {"main": [[{"node": "Classificar mensagem (API + IA)", "type": "main", "index": 0}]]},
    "Classificar mensagem (API + IA)": {
        "main": [
            [{"node": "Rotear por setor", "type": "main", "index": 0}],
            [{"node": "Preparar erro", "type": "main", "index": 0}],
        ]
    },
    "Preparar erro": {"main": [[{"node": "Planilha: Revisão humana", "type": "main", "index": 0}]]},
    "Rotear por setor": {
        "main": [[{"node": "Planilha: Revisão humana", "type": "main", "index": 0}]]
        + [[{"node": f"Planilha: {d}", "type": "main", "index": 0}] for d in DEPARTMENTS]
    },
}

workflow = {
    "id": "kodieClassifier01",
    "name": "Classificador de mensagens (Kodie)",
    "nodes": nodes,
    "connections": connections,
    "active": False,
    "settings": {"executionOrder": "v1"},
}

OUT.parent.mkdir(exist_ok=True)
OUT.write_text(json.dumps(workflow, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Gerado: {OUT} ({len(nodes)} nodes)")
