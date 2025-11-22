"""
Controlador de eventos: listado y generación de subclips.
"""
from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.shared.db import get_session
from app.shared.security import get_current_user_id
from app.survillance.infrastructure.repositories import EventoRepository, ClipRepository
from app.survillance.application.services.evento_service import EventoService
from app.survillance.application.dto import EventoResponse


router = APIRouter(prefix="/api/eventos", tags=["Eventos"])


@router.get("/{id_evento}", response_model=EventoResponse)
async def get_evento(
    id_evento: int,
    session: AsyncSession = Depends(get_session),
    user_id: int = Depends(get_current_user_id)
):
    """Obtiene un evento por ID"""
    evento_repo = EventoRepository(session)
    clip_repo = ClipRepository(session)
    service = EventoService(evento_repo, clip_repo)
    
    evento = await service.get_by_id(id_evento)
    return EventoResponse.model_validate(evento)


@router.get("", response_model=List[EventoResponse])
async def list_eventos(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    id_conexion: Optional[int] = Query(None),
    tipo_evento: Optional[str] = Query(None),
    start_time: Optional[datetime] = Query(None),
    end_time: Optional[datetime] = Query(None),
    session: AsyncSession = Depends(get_session),
    user_id: int = Depends(get_current_user_id)
):
    """Lista eventos con filtros opcionales"""
    evento_repo = EventoRepository(session)
    clip_repo = ClipRepository(session)
    service = EventoService(evento_repo, clip_repo)
    
    eventos = await service.get_all(
        limit, offset, id_conexion, tipo_evento, start_time, end_time
    )
    return [EventoResponse.model_validate(e) for e in eventos]


@router.post("/{id_evento}/generar-subclip", response_model=EventoResponse)
async def generar_subclip(
    id_evento: int,
    padding: int = Query(2, ge=0, le=60),
    session: AsyncSession = Depends(get_session),
    user_id: int = Depends(get_current_user_id)
):
    """Genera un subclip para el evento (multi-clip si es necesario)"""
    evento_repo = EventoRepository(session)
    clip_repo = ClipRepository(session)
    service = EventoService(evento_repo, clip_repo)
    
    evento = await service.generar_subclip(id_evento, padding)
    return EventoResponse.model_validate(evento)