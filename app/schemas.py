from typing import Literal, Optional

from pydantic import BaseModel, Field

Category = Literal["duvida", "reclamacao", "solicitacao", "outros"]
Priority = Literal["baixa", "media", "alta", "urgente"]
Department = Literal["atendimento", "financeiro", "suporte_tecnico", "comercial"]
Sentiment = Literal["positivo", "neutro", "negativo"]


class ClassifyRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=4000, description="Mensagem do cliente")
    customer_name: Optional[str] = Field(default=None, max_length=200)
    channel: Optional[str] = Field(default=None, max_length=50, description="email, whatsapp, etc.")


class Classification(BaseModel):
    """Contrato que o modelo de IA deve devolver (usado também como JSON Schema)."""

    category: Category = Field(description="Tipo da mensagem")
    priority: Priority = Field(description="Urgência do atendimento")
    department: Department = Field(description="Setor responsável")
    sentiment: Sentiment = Field(description="Tom emocional do cliente")
    summary: str = Field(max_length=300, description="Resumo da mensagem em uma frase")
    confidence: float = Field(ge=0.0, le=1.0, description="Confiança da classificação, de 0 a 1")


class ClassifyResponse(Classification):
    needs_human_review: bool = Field(description="True quando a resposta precisa de revisão humana")
    review_reason: Optional[str] = Field(default=None, description="Motivo da revisão, se houver")
