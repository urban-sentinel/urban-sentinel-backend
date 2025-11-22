"""
Controlador CRUD de reportes.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.shared.db import get_session
from app.shared.security import get_current_user_id
from app.survillance.infrastructure.repositories import ReporteRepository
from app.survillance.application.services.reporte_service import ReporteService
from app.survillance.application.dto import *


router = APIRouter(prefix="/api/reportes", tags=["Reportes"])


@router.post("", response_model=ReporteResponse, status_code=201)
async def create_reporte(
    data: ReporteCreate,
    session: AsyncSession = Depends(get_session),
    user_id: int = Depends(get_current_user_id)
):
    """Crea un reporte"""
    reporte_repo = ReporteRepository(session)
    service = ReporteService(reporte_repo)
    
    reporte = await service.create(data, user_id)
    return ReporteResponse.model_validate(reporte)


@router.get("", response_model=List[ReporteResponse])
async def list_reportes(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    id_usuario: Optional[int] = Query(None),
    session: AsyncSession = Depends(get_session),
    user_id: int = Depends(get_current_user_id)
):
    """Lista reportes con filtros opcionales"""
    reporte_repo = ReporteRepository(session)
    service = ReporteService(reporte_repo)
    
    # Si no se especifica id_usuario, usar el del token
    filter_user_id = id_usuario if id_usuario is not None else None
    
    reportes = await service.get_all(limit, offset, filter_user_id)
    return [ReporteResponse.model_validate(r) for r in reportes]