"""
Controlador de administración: start/stop de ingesta y retención.
"""
from typing import Dict
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.shared.db import get_session
from app.shared.security import get_current_user_id
from app.survillance.infrastructure.repositories import (
    ConexionRepository,
    ClipRepository
)
from app.survillance.application.retention_service import RetentionService
from app.survillance.ingestion.camera_supervisor import camera_supervisor
from app.survillance.ingestion.retention_job import retention_job


router = APIRouter(prefix="/api/admin", tags=["Administración"])


@router.post("/cameras/start")
async def start_cameras(
    user_id: int = Depends(get_current_user_id)
) -> Dict:
    """Inicia ingesta para todas las cámaras habilitadas"""
    await camera_supervisor.start_all()
    
    return {
        "message": "Ingesta iniciada para todas las cámaras habilitadas",
        "status": camera_supervisor.get_status()
    }


@router.post("/cameras/{id_conexion}/start")
async def start_camera(
    id_conexion: int,
    user_id: int = Depends(get_current_user_id)
) -> Dict:
    """Inicia ingesta para una cámara específica"""
    await camera_supervisor.start_camera(id_conexion)
    
    return {
        "message": f"Ingesta iniciada para cámara {id_conexion}",
        "running": camera_supervisor.is_camera_running(id_conexion)
    }


@router.post("/cameras/{id_conexion}/stop")
async def stop_camera(
    id_conexion: int,
    user_id: int = Depends(get_current_user_id)
) -> Dict:
    """Detiene ingesta de una cámara específica"""
    await camera_supervisor.stop_camera(id_conexion)
    
    return {
        "message": f"Ingesta detenida para cámara {id_conexion}",
        "running": camera_supervisor.is_camera_running(id_conexion)
    }


@router.post("/cameras/stop")
async def stop_cameras(
    user_id: int = Depends(get_current_user_id)
) -> Dict:
    """Detiene ingesta de todas las cámaras"""
    await camera_supervisor.stop_all()
    
    return {
        "message": "Ingesta detenida para todas las cámaras",
        "status": camera_supervisor.get_status()
    }


@router.get("/cameras/status")
async def get_cameras_status(
    user_id: int = Depends(get_current_user_id)
) -> Dict:
    """Obtiene el estado de ingesta de todas las cámaras"""
    return {
        "cameras": camera_supervisor.get_status()
    }


@router.post("/retention/apply")
async def apply_retention(
    session: AsyncSession = Depends(get_session),
    user_id: int = Depends(get_current_user_id)
) -> Dict:
    """Aplica retención manualmente (elimina clips viejos)"""
    conexion_repo = ConexionRepository(session)
    clip_repo = ClipRepository(session)
    
    retention_service = RetentionService(conexion_repo, clip_repo)
    stats = await retention_service.apply_retention()
    
    return {
        "message": "Retención aplicada",
        "deleted_clips": stats["deleted_clips"],
        "deleted_files": stats["deleted_files"],
        "errors": stats["errors"]
    }


@router.get("/retention/status")
async def get_retention_status(
    session: AsyncSession = Depends(get_session),
    user_id: int = Depends(get_current_user_id)
) -> Dict:
    """Obtiene el estado de retención de todas las cámaras"""
    conexion_repo = ConexionRepository(session)
    clip_repo = ClipRepository(session)
    
    retention_service = RetentionService(conexion_repo, clip_repo)
    status = await retention_service.get_retention_status()
    
    return {
        "cameras": status
    }


@router.post("/retention/start")
async def start_retention_job(
    user_id: int = Depends(get_current_user_id)
) -> Dict:
    """Inicia el job periódico de retención"""
    await retention_job.start()
    
    return {
        "message": "Job de retención iniciado",
        "interval_seconds": retention_job.interval_seconds
    }


@router.post("/retention/stop")
async def stop_retention_job(
    user_id: int = Depends(get_current_user_id)
) -> Dict:
    """Detiene el job periódico de retención"""
    await retention_job.stop()
    
    return {
        "message": "Job de retención detenido"
    }