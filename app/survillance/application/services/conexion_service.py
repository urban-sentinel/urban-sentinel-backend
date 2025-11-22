"""
Servicio CRUD de conexiones/cámaras.
"""
from typing import List, Optional

from fastapi import HTTPException, status


from app.shared.time import now_utc
from app.survillance.domain.entities.connection import Conexion
from app.survillance.domain.repositories_interfaces import IConexionRepository
from app.survillance.domain.enums import ModoIngesta
from app.survillance.application.dto import ConexionCreate, ConexionUpdate


class ConexionService:
    """Servicio CRUD de conexiones/cámaras"""
    
    def __init__(self, conexion_repo: IConexionRepository):
        self.conexion_repo = conexion_repo
    
    async def create(self, data: ConexionCreate) -> Conexion:
        """Crea una conexión"""
        # Convertir string a enum
        modo_ingesta_enum = ModoIngesta(data.modo_ingesta) if isinstance(data.modo_ingesta, str) else data.modo_ingesta
        conexion = Conexion(
            id_oficina=data.id_oficina,
            nombre_camara=data.nombre_camara,
            ubicacion=data.ubicacion,
            rtsp_url=data.rtsp_url,
            estado="inactiva",
            modo_ingesta=modo_ingesta_enum,
            fps_sample=data.fps_sample,
            habilitada=data.habilitada,
            retention_minutes=data.retention_minutes,
            created_at=now_utc()
        )
        return await self.conexion_repo.create(conexion)
    
    async def get_by_id(self, id_conexion: int) -> Conexion:
        """Obtiene conexión por ID"""
        conexion = await self.conexion_repo.get_by_id(id_conexion)
        if not conexion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conexión no encontrada"
            )
        return conexion
    
    async def get_all(
        self,
        limit: int = 100,
        offset: int = 0,
        id_oficina: Optional[int] = None,
        habilitada: Optional[bool] = None
    ) -> List[Conexion]:
        """Lista todas las conexiones con filtros"""
        return await self.conexion_repo.get_all(limit, offset, id_oficina, habilitada)
    
    async def update(self, id_conexion: int, data: ConexionUpdate) -> Conexion:
        """Actualiza una conexión"""
        conexion = await self.get_by_id(id_conexion)
        
        if data.nombre_camara is not None:
            conexion.nombre_camara = data.nombre_camara
        if data.ubicacion is not None:
            conexion.ubicacion = data.ubicacion
        if data.rtsp_url is not None:
            conexion.rtsp_url = data.rtsp_url
        if data.estado is not None:
            conexion.estado = data.estado
        if data.modo_ingesta is not None:
            # Convertir string a enum si es necesario
            conexion.modo_ingesta = ModoIngesta(data.modo_ingesta) if isinstance(data.modo_ingesta, str) else data.modo_ingesta
        if data.fps_sample is not None:
            conexion.fps_sample = data.fps_sample
        if data.habilitada is not None:
            conexion.habilitada = data.habilitada
        if data.retention_minutes is not None:
            conexion.retention_minutes = data.retention_minutes
        
        conexion.updated_at = now_utc()
        
        return await self.conexion_repo.update(conexion)
    
    async def delete(self, id_conexion: int) -> bool:
        """Elimina una conexión"""
        return await self.conexion_repo.delete(id_conexion)

