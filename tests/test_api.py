import json

import pytest
from fastapi.testclient import TestClient

from app.classifier import LLMError
from app.config import Settings
from app.main import app, get_llm, get_settings

GOOD = {
    "category": "reclamacao",
    "priority": "urgente",
    "department": "financeiro",
    "sentiment": "negativo",
    "summary": "Cliente relata cobrança em duplicidade.",
    "confidence": 0.95,
}


class FakeLLM:
    def __init__(self, output=None, error=None):
        self.output, self.error, self.calls = output, error, []

    def generate_json(self, system_prompt, user_prompt):
        self.calls.append((system_prompt, user_prompt))
        if self.error:
            raise self.error
        return self.output


@pytest.fixture
def client():
    app.dependency_overrides[get_settings] = lambda: Settings(confidence_threshold=0.6)
    yield TestClient(app)
    app.dependency_overrides.clear()


def use(llm):
    app.dependency_overrides[get_llm] = lambda: llm
    return llm


def test_health(client):
    assert client.get("/health").json() == {"status": "ok"}


def test_classify_ok(client):
    llm = use(FakeLLM(json.dumps(GOOD)))
    r = client.post("/classify", json={"message": "Fui cobrado duas vezes!"})
    assert r.status_code == 200
    body = r.json()
    assert body["category"] == "reclamacao"
    assert body["department"] == "financeiro"
    assert body["needs_human_review"] is False
    assert "Fui cobrado duas vezes!" in llm.calls[0][1]


def test_low_confidence_flags_review(client):
    use(FakeLLM(json.dumps({**GOOD, "confidence": 0.3})))
    body = client.post("/classify", json={"message": "oi"}).json()
    assert body["needs_human_review"] is True
    assert body["review_reason"]


@pytest.mark.parametrize(
    "raw",
    ["não é json", json.dumps({**GOOD, "category": "inventada"}), json.dumps({"category": "duvida"})],
)
def test_invalid_ai_output_falls_back(client, raw):
    use(FakeLLM(raw))
    r = client.post("/classify", json={"message": "teste"})
    assert r.status_code == 200
    body = r.json()
    assert body["needs_human_review"] is True
    assert body["confidence"] == 0.0


def test_provider_failure_returns_502(client):
    use(FakeLLM(error=LLMError("Gemini respondeu HTTP 429")))
    r = client.post("/classify", json={"message": "teste"})
    assert r.status_code == 502


@pytest.mark.parametrize("payload", [{}, {"message": ""}, {"message": "x" * 4001}])
def test_input_validation(client, payload):
    use(FakeLLM(json.dumps(GOOD)))
    assert client.post("/classify", json=payload).status_code == 422
