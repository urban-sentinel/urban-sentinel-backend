"""
Controlador de webhook de inferencia: acepta contratos A y B.
"""
from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.shared.db import get_session
from app.survillance.infrastructure.repositories import (
    EventoRepository,
    ClipRepository,
    InferenceRequestRepository
)
from app.survillance.application.inference_service import InferenceService
from app.survillance.application.dto import InferenceWebhookResponse


router = APIRouter(prefix="/api/inferencia", tags=["Inferencia"])


@router.post("/resultados", response_model=InferenceWebhookResponse)
async def recibir_resultados(
    request: Request,
    session: AsyncSession = Depends(get_session)
):
    """
    Recibe resultados de inferencia de IA.
    Detecta automáticamente contrato A (offsets relativos) o B (timestamps absolutos).
    """
    # Obtener payload como dict
    payload = await request.json()
    
    # Crear servicio
    evento_repo = EventoRepository(session)
    clip_repo = ClipRepository(session)
    inference_repo = InferenceRequestRepository(session)
    
    service = InferenceService(evento_repo, clip_repo, inference_repo)
    
    # Procesar webhook (detecta contrato automáticamente)
    response = await service.process_webhook(payload)
    
    return response