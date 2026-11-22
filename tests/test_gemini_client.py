"""Tentativas e modelo de reserva do GeminiClient, sem rede (httpx.post substituído)."""
import httpx
import pytest

from app import classifier
from app.classifier import GeminiClient, LLMError
from app.config import Settings

OK_TEXT = '{"category":"duvida"}'


def _ok():
    return httpx.Response(200, json={"candidates": [{"content": {"parts": [{"text": OK_TEXT}]}}]})


@pytest.fixture
def calls(monkeypatch):
    monkeypatch.setattr(classifier.time, "sleep", lambda s: None)
    log = []

    def install(*outcomes):
        seq = iter(outcomes)

        def fake_post(url, **kwargs):
            log.append(url.split("/models/")[1].split(":")[0])
            out = next(seq)
            if isinstance(out, Exception):
                raise out
            return out

        monkeypatch.setattr(classifier.httpx, "post", fake_post)
        return log

    return install


def _client(**kw):
    base = dict(gemini_api_key="x", gemini_model="principal", gemini_fallback_model="reserva",
                gemini_attempts_per_model=2)
    return GeminiClient(Settings(_env_file=None, **{**base, **kw}))


def test_retries_same_model_after_503(calls):
    log = calls(httpx.Response(503), _ok())
    assert _client().generate_json("s", "u") == OK_TEXT
    assert log == ["principal", "principal"]


def test_falls_back_to_second_model(calls):
    log = calls(httpx.Response(503), httpx.ReadTimeout("t"), _ok())
    assert _client().generate_json("s", "u") == OK_TEXT
    assert log == ["principal", "principal", "reserva"]


def test_404_skips_straight_to_fallback(calls):
    log = calls(httpx.Response(404), _ok())
    assert _client().generate_json("s", "u") == OK_TEXT
    assert log == ["principal", "reserva"]


def test_auth_error_does_not_retry(calls):
    log = calls(httpx.Response(403))
    with pytest.raises(LLMError, match="403"):
        _client().generate_json("s", "u")
    assert log == ["principal"]


def test_all_attempts_fail_raises_last_error(calls):
    log = calls(*[httpx.Response(503)] * 4)
    with pytest.raises(LLMError, match=r"reserva.*503"):
        _client().generate_json("s", "u")
    assert log == ["principal", "principal", "reserva", "reserva"]
