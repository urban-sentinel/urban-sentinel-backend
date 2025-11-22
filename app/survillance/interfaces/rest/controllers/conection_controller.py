"""
Controlador CRUD de conexiones/cámaras.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.shared.db import get_session
from app.shared.security import get_current_user_id
from app.survillance.infrastructure.repositories import ConexionRepository
from app.survillance.application.services.conexion_service import ConexionService
from app.survillance.application.dto import *


router = APIRouter(prefix="/api/conexiones", tags=["Conexiones"])


@router.post("", response_model=ConexionResponse, status_code=201)
async def create_conexion(
    data: ConexionCreate,
    session: AsyncSession = Depends(get_session),
    user_id: int = Depends(get_current_user_id)
):
    """Crea una nueva conexión/cámara"""
    conexion_repo = ConexionRepository(session)
    service = ConexionService(conexion_repo)
    
    conexion = await service.create(data)
    return ConexionResponse.model_validate(conexion)


@router.get("/{id_conexion}", response_model=ConexionResponse)
async def get_conexion(
    id_conexion: int,
    session: AsyncSession = Depends(get_session),
    user_id: int = Depends(get_current_user_id)
):
    """Obtiene una conexión por ID"""
    conexion_repo = ConexionRepository(session)
    service = ConexionService(conexion_repo)
    
    conexion = await service.get_by_id(id_conexion)
    return ConexionResponse.model_validate(conexion)


@router.get("", response_model=List[ConexionResponse])
async def list_conexiones(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    id_oficina: Optional[int] = Query(None),
    habilitada: Optional[bool] = Query(None),
    session: AsyncSession = Depends(get_session),
    user_id: int = Depends(get_current_user_id)
):
    """Lista todas las conexiones con filtros opcionales"""
    conexion_repo = ConexionRepository(session)
    service = ConexionService(conexion_repo)
    
    conexiones = await service.get_all(limit, offset, id_oficina, habilitada)
    return [ConexionResponse.model_validate(c) for c in conexiones]

@router.patch("/{id_conexion}/habilitada", response_model=ConexionResponse)
async def update_habilitada(
    id_conexion: int,
    habilitada: bool = Query(..., description="True para habilitar la cámara, False para deshabilitarla"),
    session: AsyncSession = Depends(get_session),
    user_id: int = Depends(get_current_user_id)
):
    """
    Actualiza el permiso de la cámara (habilitada/deshabilitada).
    """
    conexion_repo = ConexionRepository(session)
    service = ConexionService(conexion_repo)
    
    # Creamos el DTO solo con el campo habilitada
    update_data = ConexionUpdate(habilitada=habilitada)
    
    # El servicio detectará que solo 'habilitada' tiene valor y solo actualizará eso
    conexion = await service.update(id_conexion, update_data)
    
    return ConexionResponse.model_validate(conexion)

@router.patch("/{id_conexion}/estado", response_model=ConexionResponse)
async def update_estado(
    id_conexion: int,
    activo: bool = Query(..., description="True para poner estado 'running', False para 'stopped'"),
    session: AsyncSession = Depends(get_session),
    user_id: int = Depends(get_current_user_id)
):
    """
    Actualiza el estado visual (running/stopped) sin tocar la configuración.
    """
    conexion_repo = ConexionRepository(session)
    service = ConexionService(conexion_repo)
    
    # Mapeamos el booleano a los strings que usas en tu DB
    nuevo_estado = "activa" if activo else "inactiva"
    
    # Creamos el DTO solo con el campo estado
    update_data = ConexionUpdate(estado=nuevo_estado)
    
    # El servicio solo actualizará el campo 'estado'
    conexion = await service.update(id_conexion, update_data)
    
    return ConexionResponse.model_validate(conexion)

@router.put("/{id_conexion}", response_model=ConexionResponse)
async def update_conexion(
    id_conexion: int,
    data: ConexionUpdate,
    session: AsyncSession = Depends(get_session),
    user_id: int = Depends(get_current_user_id)
):
    """Actualiza una conexión"""
    conexion_repo = ConexionRepository(session)
    service = ConexionService(conexion_repo)
    
    conexion = await service.update(id_conexion, data)
    return ConexionResponse.model_validate(conexion)

@router.delete("/{id_conexion}", status_code=204)
async def delete_conexion(
    id_conexion: int,
    session: AsyncSession = Depends(get_session),
    user_id: int = Depends(get_current_user_id)
):
    """Elimina una conexión"""
    conexion_repo = ConexionRepository(session)
    service = ConexionService(conexion_repo)
    
    await service.delete(id_conexion)