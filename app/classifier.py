import json
import time
from typing import Protocol

import httpx
from pydantic import ValidationError

from .config import Settings
from .prompt import SYSTEM_PROMPT, build_user_prompt
from .schemas import Classification, ClassifyRequest, ClassifyResponse

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
# Sobrecarga, cota e falha do lado do Google: vale tentar de novo.
RETRYABLE_STATUS = {429, 500, 502, 503, 504}
# Modelo inexistente/desativado: não adianta repetir, mas o de reserva pode funcionar.
NEXT_MODEL_STATUS = RETRYABLE_STATUS | {404}
BACKOFF_SECONDS = 1.5


class LLMError(Exception):
    """Falha ao falar com o provedor de IA (rede, autenticação, cota, resposta vazia)."""

    def __init__(self, message: str, status: int | None = None, network: bool = False):
        super().__init__(message)
        self.status = status
        self.network = network


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
        models = [self._settings.gemini_model]
        fallback = self._settings.gemini_fallback_model
        if fallback and fallback not in models:
            models.append(fallback)

        last: LLMError | None = None
        for model in models:
            for attempt in range(max(1, self._settings.gemini_attempts_per_model)):
                if attempt:
                    time.sleep(BACKOFF_SECONDS * attempt)
                try:
                    return self._call(model, body)
                except LLMError as exc:
                    last = exc
                    if not (exc.network or exc.status in RETRYABLE_STATUS):
                        break
            if not (last.network or last.status in NEXT_MODEL_STATUS):
                break
        raise last

    def _call(self, model: str, body: dict) -> str:
        url = GEMINI_URL.format(model=model)
        try:
            resp = httpx.post(
                url,
                json=body,
                headers={"x-goog-api-key": self._settings.gemini_api_key},
                timeout=self._settings.gemini_timeout_seconds,
            )
        except httpx.HTTPError as exc:
            raise LLMError(
                f"Erro de rede ao chamar o Gemini ({model}): {type(exc).__name__}", network=True
            ) from exc

        if resp.status_code != 200:
            # Não repassa o corpo inteiro para não vazar detalhes internos nos logs/respostas.
            raise LLMError(f"Gemini ({model}) respondeu HTTP {resp.status_code}", status=resp.status_code)

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
