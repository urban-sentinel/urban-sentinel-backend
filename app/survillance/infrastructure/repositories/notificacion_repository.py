"""
Repositorio de Notificacion: implementación con SQLAlchemy.
"""
from typing import Optional, Sequence, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.survillance.models import Notificacion as NotificacionORM
from app.survillance.domain.entities.notification import Notificacion
from app.survillance.domain.mappers import notificacion_to_domain, notificacion_to_orm


class NotificacionRepository:
    """Adaptador de repositorio de notificaciones usando entidades de dominio"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get(self, id: int) -> Optional[Notificacion]:
        """Obtiene una notificación por ID"""
        result = await self.session.execute(
            select(NotificacionORM).where(NotificacionORM.id_notificacion == id)
        )
        orm = result.scalar_one_or_none()
        return notificacion_to_domain(orm) if orm else None
    
    async def get_by_id(self, id: int) -> Optional[Notificacion]:
        """Obtiene una notificación por ID (alias para servicios)"""
        return await self.get(id)
    
    async def list(
        self,
        limit: int = 50,
        offset: int = 0
    ) -> Sequence[Notificacion]:
        """Lista notificaciones con filtros opcionales"""
        query = select(NotificacionORM)
        
        query = query.limit(limit).offset(offset)
        result = await self.session.execute(query)
        return [notificacion_to_domain(orm) for orm in result.scalars().all()]
    
    async def get_all(
        self,
        limit: int = 100,
        offset: int = 0
    ) -> List[Notificacion]:
        """Lista todas las notificaciones con filtros (alias para servicios)"""
        return list(await self.list(limit, offset))
    
    async def save(self, notificacion: Notificacion) -> Notificacion:
        """
        Guarda una notificación (crea o actualiza según si tiene ID).
        Si entity.id is None: crea nuevo registro.
        Si entity.id is not None: actualiza registro existente.
        """
        if notificacion.id is None:
            # Nueva entidad: crear modelo sin ID
            model = notificacion_to_orm(notificacion)
            self.session.add(model)
        else:
            # Entidad existente: buscar o crear modelo y actualizar
            result = await self.session.execute(
                select(NotificacionORM).where(NotificacionORM.id_notificacion == notificacion.id)
            )
            existing_orm = result.scalar_one_or_none()
            model = notificacion_to_orm(notificacion, existing_orm)
            if existing_orm is None:
                self.session.add(model)
        
        await self.session.flush()
        await self.session.refresh(model)
        
        return notificacion_to_domain(model)
    
    async def create(self, notificacion: Notificacion) -> Notificacion:
        """Crea una nueva notificación (alias para compatibilidad)"""
        return await self.save(notificacion)
    
    async def update(self, notificacion: Notificacion) -> Notificacion:
        """Actualiza una notificación existente (alias para compatibilidad)"""
        if notificacion.id is None:
            raise ValueError("No se puede actualizar una notificación sin ID")
        return await self.save(notificacion)


