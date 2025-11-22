"""
Repositorio de Clip: implementación con SQLAlchemy.
"""
from typing import Optional, Sequence, List
from datetime import datetime

from sqlalchemy import select, delete as sql_delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.survillance.models import Clip as ClipORM
from app.survillance.domain.entities.clip import Clip
from app.survillance.domain.mappers import clip_to_domain, clip_to_orm


class ClipRepository:
    """Adaptador de repositorio de clips usando entidades de dominio"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get(self, id: int) -> Optional[Clip]:
        """Obtiene un clip por ID"""
        result = await self.session.execute(
            select(ClipORM).where(ClipORM.id_clip == id)
        )
        orm = result.scalar_one_or_none()
        return clip_to_domain(orm) if orm else None
    
    async def get_by_id(self, id: int) -> Optional[Clip]:
        """Obtiene un clip por ID (alias para servicios)"""
        return await self.get(id)
    
    async def list(
        self,
        limit: int = 50,
        offset: int = 0,
        id_conexion: Optional[int] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> Sequence[Clip]:
        """Lista clips con filtros opcionales"""
        query = select(ClipORM)
        
        if id_conexion is not None:
            query = query.where(ClipORM.id_conexion == id_conexion)
        
        if start_time is not None:
            query = query.where(ClipORM.start_time_utc >= start_time)
        
        if end_time is not None:
            query = query.where(ClipORM.start_time_utc <= end_time)
        
        query = query.order_by(ClipORM.start_time_utc.desc()).limit(limit).offset(offset)
        result = await self.session.execute(query)
        return [clip_to_domain(orm) for orm in result.scalars().all()]
    
    async def get_all(
        self,
        limit: int = 100,
        offset: int = 0,
        id_conexion: Optional[int] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> List[Clip]:
        """Lista todos los clips con filtros (alias para servicios)"""
        return list(await self.list(limit, offset, id_conexion, start_time, end_time))
    
    async def find_by_time_range(
        self,
        id_conexion: int,
        start_time: datetime,
        end_time: datetime
    ) -> Sequence[Clip]:
        """Encuentra clips que intersectan con un rango de tiempo"""
        result = await self.session.execute(
            select(ClipORM)
            .where(ClipORM.id_conexion == id_conexion)
            .where(ClipORM.start_time_utc < end_time)
            .order_by(ClipORM.start_time_utc)
        )
        return [clip_to_domain(orm) for orm in result.scalars().all()]
    
    async def get_by_time_range(
        self,
        id_conexion: int,
        start_time: datetime,
        end_time: datetime
    ) -> List[Clip]:
        """Alias para servicios"""
        return list(await self.find_by_time_range(id_conexion, start_time, end_time))
    
    async def find_old_clips(
        self,
        id_conexion: int,
        older_than: datetime
    ) -> Sequence[Clip]:
        """Encuentra clips más antiguos que una fecha"""
        result = await self.session.execute(
            select(ClipORM)
            .where(ClipORM.id_conexion == id_conexion)
            .where(ClipORM.fecha_guardado < older_than)
        )
        return [clip_to_domain(orm) for orm in result.scalars().all()]
    
    async def save(self, clip: Clip) -> Clip:
        """
        Guarda un clip (crea o actualiza según si tiene ID).
        Si entity.id is None: crea nuevo registro.
        Si entity.id is not None: actualiza registro existente.
        """
        if clip.id is None:
            # Nueva entidad: crear modelo sin ID
            model = clip_to_orm(clip)
            self.session.add(model)
        else:
            # Entidad existente: buscar o crear modelo y actualizar
            result = await self.session.execute(
                select(ClipORM).where(ClipORM.id_clip == clip.id)
            )
            existing_orm = result.scalar_one_or_none()
            model = clip_to_orm(clip, existing_orm)
            if existing_orm is None:
                self.session.add(model)
        
        await self.session.flush()
        await self.session.refresh(model)
        
        return clip_to_domain(model)
    
    async def create(self, clip: Clip) -> Clip:
        """Crea un nuevo clip (alias para compatibilidad)"""
        return await self.save(clip)
    
    async def delete(self, id: int) -> None:
        """Elimina un clip"""
        await self.session.execute(
            sql_delete(ClipORM).where(ClipORM.id_clip == id)
        )



