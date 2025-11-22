"""
Repositorio de Evento: implementación con SQLAlchemy.
"""
from typing import Optional, Sequence, List
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.survillance.models import Evento as EventoORM
from app.survillance.domain.entities.event import Evento
from app.survillance.domain.mappers import evento_to_domain, evento_to_orm


class EventoRepository:
    """Adaptador de repositorio de eventos usando entidades de dominio"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get(self, id: int) -> Optional[Evento]:
        """Obtiene un evento por ID"""
        result = await self.session.execute(
            select(EventoORM).where(EventoORM.id_evento == id)
        )
        orm = result.scalar_one_or_none()
        return evento_to_domain(orm) if orm else None
    
    async def get_by_id(self, id: int) -> Optional[Evento]:
        """Obtiene un evento por ID (alias para servicios)"""
        return await self.get(id)
    
    async def list(
        self,
        limit: int = 50,
        offset: int = 0,
        id_conexion: Optional[int] = None,
        tipo_evento: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> Sequence[Evento]:
        """Lista eventos con filtros opcionales"""
        query = select(EventoORM)
        
        if id_conexion is not None:
            query = query.where(EventoORM.id_conexion == id_conexion)
        
        if tipo_evento is not None:
            query = query.where(EventoORM.tipo_evento == tipo_evento)
        
        if start_time is not None:
            query = query.where(EventoORM.timestamp_evento >= start_time)
        
        if end_time is not None:
            query = query.where(EventoORM.timestamp_evento <= end_time)
        
        query = query.order_by(EventoORM.timestamp_evento.desc()).limit(limit).offset(offset)
        result = await self.session.execute(query)
        return [evento_to_domain(orm) for orm in result.scalars().all()]
    
    async def get_all(
        self,
        limit: int = 100,
        offset: int = 0,
        id_conexion: Optional[int] = None,
        tipo_evento: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> List[Evento]:
        """Lista todos los eventos con filtros (alias para servicios)"""
        return list(await self.list(limit, offset, id_conexion, tipo_evento, start_time, end_time))
    
    async def save(self, evento: Evento) -> Evento:
        """
        Guarda un evento (crea o actualiza según si tiene ID).
        Si entity.id is None: crea nuevo registro.
        Si entity.id is not None: actualiza registro existente.
        """
        if evento.id is None:
            # Nueva entidad: crear modelo sin ID
            model = evento_to_orm(evento)
            self.session.add(model)
        else:
            # Entidad existente: buscar o crear modelo y actualizar
            result = await self.session.execute(
                select(EventoORM).where(EventoORM.id_evento == evento.id)
            )
            existing_orm = result.scalar_one_or_none()
            model = evento_to_orm(evento, existing_orm)
            if existing_orm is None:
                self.session.add(model)
        
        await self.session.flush()
        await self.session.refresh(model)
        
        return evento_to_domain(model)
    
    async def create(self, evento: Evento) -> Evento:
        """Crea un nuevo evento (alias para compatibilidad)"""
        return await self.save(evento)
    
    async def update(self, evento: Evento) -> Evento:
        """Actualiza un evento existente (alias para compatibilidad)"""
        if evento.id is None:
            raise ValueError("No se puede actualizar un evento sin ID")
        return await self.save(evento)


