"""
Controlador CRUD de notificaciones.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.shared.db import get_session
from app.shared.security import get_current_user_id
from app.survillance.infrastructure.repositories import NotificacionRepository
from app.survillance.application.services.notificacion_service import NotificacionService
from app.survillance.application.dto import *


router = APIRouter(prefix="/api/notificaciones", tags=["Notificaciones"])


@router.post("", response_model=NotificacionResponse, status_code=201)
async def create_notificacion(
    data: NotificacionCreate,
    session: AsyncSession = Depends(get_session),
    user_id: int = Depends(get_current_user_id)
):
    """Crea una notificación"""
    notif_repo = NotificacionRepository(session)
    service = NotificacionService(notif_repo)
    
    notif = await service.create(data)
    return NotificacionResponse.model_validate(notif)


@router.get("", response_model=List[NotificacionResponse])
async def list_notificaciones(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    session: AsyncSession = Depends(get_session),
    user_id: int = Depends(get_current_user_id)
):
    """Lista notificaciones con filtros opcionales"""
    notif_repo = NotificacionRepository(session)
    service = NotificacionService(notif_repo)
    
    notificaciones = await service.get_all(limit, offset)
    return [NotificacionResponse.model_validate(n) for n in notificaciones]


@router.put("/{id_notificacion}", response_model=NotificacionResponse)
async def update_notificacion(
    id_notificacion: int,
    data: NotificacionUpdate,
    session: AsyncSession = Depends(get_session),
    user_id: int = Depends(get_current_user_id)
):
    """Actualiza una notificación"""
    notif_repo = NotificacionRepository(session)
    service = NotificacionService(notif_repo)
    
    notif = await service.update(id_notificacion, data)
    return NotificacionResponse.model_validate(notif)