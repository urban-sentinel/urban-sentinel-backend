"""
Controlador de clips: listado y búsqueda.
"""
from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.shared.db import get_session
from app.shared.security import get_current_user_id
from app.survillance.infrastructure.repositories import ClipRepository
from app.survillance.application.services.clip_service import ClipService
from app.survillance.application.dto import ClipResponse


router = APIRouter(prefix="/api/clips", tags=["Clips"])


@router.get("/{id_clip}", response_model=ClipResponse)
async def get_clip(
    id_clip: int,
    session: AsyncSession = Depends(get_session),
    user_id: int = Depends(get_current_user_id)
):
    """Obtiene un clip por ID"""
    clip_repo = ClipRepository(session)
    service = ClipService(clip_repo)
    
    clip = await service.get_by_id(id_clip)
    return ClipResponse.model_validate(clip)


@router.get("", response_model=List[ClipResponse])
async def list_clips(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    id_conexion: Optional[int] = Query(None),
    start_time: Optional[datetime] = Query(None),
    end_time: Optional[datetime] = Query(None),
    session: AsyncSession = Depends(get_session),
    user_id: int = Depends(get_current_user_id)
):
    """Lista clips con filtros opcionales"""
    clip_repo = ClipRepository(session)
    service = ClipService(clip_repo)
    
    clips = await service.get_all(limit, offset, id_conexion, start_time, end_time)
    return [ClipResponse.model_validate(c) for c in clips]