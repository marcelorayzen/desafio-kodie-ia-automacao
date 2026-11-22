import json
from typing import Protocol

import httpx
from pydantic import ValidationError

from .config import Settings
from .prompt import SYSTEM_PROMPT, build_user_prompt
from .schemas import Classification, ClassifyRequest, ClassifyResponse

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"


class LLMError(Exception):
    """Falha ao falar com o provedor de IA (rede, autenticação, cota, resposta vazia)."""


class LLMClient(Protocol):
    def generate_json(self, system_prompt: str, user_prompt: str) -> str: ...


class GeminiClient:
    def __init__(self, settings: Settings):
        self._settings = settings

    def generate_json(self, system_prompt: str, user_prompt: str) -> str:
        if not self._settings.gemini_api_key:
            raise LLMError("GEMINI_API_KEY não configurada")

        body = {
            "systemInstruction": {"parts": [{"text": system_prompt}]},
            "contents": [{"role": "user", "parts": [{"text": user_prompt}]}],
            "generationConfig": {
                "temperature": 0,
                "responseMimeType": "application/json",
                "responseJsonSchema": Classification.model_json_schema(),
            },
        }
        if self._settings.gemini_thinking_level:
            body["generationConfig"]["thinkingConfig"] = {
                "thinkingLevel": self._settings.gemini_thinking_level
            }
        url = GEMINI_URL.format(model=self._settings.gemini_model)
        try:
            resp = httpx.post(
                url,
                json=body,
                headers={"x-goog-api-key": self._settings.gemini_api_key},
                timeout=self._settings.gemini_timeout_seconds,
            )
        except httpx.HTTPError as exc:
            raise LLMError(f"Erro de rede ao chamar o Gemini: {type(exc).__name__}") from exc

        if resp.status_code != 200:
            # Não repassa o corpo inteiro para não vazar detalhes internos nos logs/respostas.
            raise LLMError(f"Gemini respondeu HTTP {resp.status_code}")

        try:
            return resp.json()["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError, ValueError) as exc:
            raise LLMError("Resposta do Gemini sem texto utilizável") from exc


def _fallback(reason: str) -> ClassifyResponse:
    return ClassifyResponse(
        category="outros",
        priority="media",
        department="atendimento",
        sentiment="neutro",
        summary="Não foi possível classificar automaticamente.",
        confidence=0.0,
        needs_human_review=True,
        review_reason=reason,
    )


def classify_message(req: ClassifyRequest, llm: LLMClient, settings: Settings) -> ClassifyResponse:
    raw = llm.generate_json(SYSTEM_PROMPT, build_user_prompt(req.message, req.customer_name, req.channel))

    try:
        result = Classification.model_validate(json.loads(raw))
    except (json.JSONDecodeError, ValidationError):
        return _fallback("Resposta da IA fora do formato esperado")

    low_confidence = result.confidence < settings.confidence_threshold
    return ClassifyResponse(
        **result.model_dump(),
        needs_human_review=low_confidence,
        review_reason="Confiança abaixo do limite" if low_confidence else None,
    )
