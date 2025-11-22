"""
DTOs para Inference Webhook.
"""
from typing import Optional, List
from pydantic import BaseModel


class EventoInferenciaBase(BaseModel):
    """Base para eventos de inferencia"""
    tipo: str
    confianza: float


class EventoInferenciaA(EventoInferenciaBase):
    """Contrato A: offsets relativos al clip"""
    t_inicio_ms: int
    t_fin_ms: int


class EventoInferenciaB(EventoInferenciaBase):
    """Contrato B: timestamp absoluto"""
    timestamp_utc: str
    dur_ms: int


class InferenceWebhookRequestA(BaseModel):
    """Request webhook con offsets relativos (Contrato A)"""
    request_id: str
    conexion_id: int
    clip_id: Optional[int] = None
    clip_path: Optional[str] = None
    modelo_version: str
    eventos: List[EventoInferenciaA]


class InferenceWebhookRequestB(BaseModel):
    """Request webhook con timestamps absolutos (Contrato B)"""
    request_id: str
    conexion_id: int
    modelo_version: str
    eventos: List[EventoInferenciaB]


class InferenceWebhookResponse(BaseModel):
    """Response de webhook de inferencia"""
    ok: bool
    created_event_ids: List[int] = []
    message: Optional[str] = None



