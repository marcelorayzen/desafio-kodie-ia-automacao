from fastapi import Depends, FastAPI, HTTPException

from .classifier import GeminiClient, LLMClient, LLMError, classify_message
from .config import Settings, get_settings
from .schemas import ClassifyRequest, ClassifyResponse

app = FastAPI(title="Classificador de Mensagens", version="1.0.0")


def get_llm(settings: Settings = Depends(get_settings)) -> LLMClient:
    return GeminiClient(settings)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/classify", response_model=ClassifyResponse)
def classify(
    req: ClassifyRequest,
    settings: Settings = Depends(get_settings),
    llm: LLMClient = Depends(get_llm),
) -> ClassifyResponse:
    try:
        return classify_message(req, llm, settings)
    except LLMError as exc:
        raise HTTPException(status_code=502, detail=f"Falha no provedor de IA: {exc}") from exc
