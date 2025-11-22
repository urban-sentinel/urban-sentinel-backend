"""
Repositorio de Oficina: implementación con SQLAlchemy.
"""
from typing import Optional, Sequence, List

from sqlalchemy import select, delete as sql_delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.survillance.models import Oficina as OficinaORM
from app.survillance.domain.entities.office import Oficina
from app.survillance.domain.mappers import oficina_to_domain, oficina_to_orm


class OficinaRepository:
    """Adaptador de repositorio de oficinas usando entidades de dominio"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get(self, id: int) -> Optional[Oficina]:
        """Obtiene una oficina por ID"""
        result = await self.session.execute(
            select(OficinaORM).where(OficinaORM.id_oficina == id)
        )
        orm = result.scalar_one_or_none()
        return oficina_to_domain(orm) if orm else None
    
    async def get_by_id(self, id: int) -> Optional[Oficina]:
        """Obtiene una oficina por ID (alias para servicios)"""
        return await self.get(id)
    
    async def list(self, limit: int = 50, offset: int = 0) -> Sequence[Oficina]:
        """Lista oficinas con paginación"""
        result = await self.session.execute(
            select(OficinaORM).limit(limit).offset(offset)
        )
        return [oficina_to_domain(orm) for orm in result.scalars().all()]
    
    async def get_all(self, limit: int = 100, offset: int = 0) -> List[Oficina]:
        """Lista todas las oficinas (alias para servicios)"""
        return list(await self.list(limit, offset))
    
    async def save(self, oficina: Oficina) -> Oficina:
        """
        Guarda una oficina (crea o actualiza según si tiene ID).
        Si entity.id is None: crea nuevo registro.
        Si entity.id is not None: actualiza registro existente.
        """
        if oficina.id is None:
            # Nueva entidad: crear modelo sin ID
            model = oficina_to_orm(oficina)
            self.session.add(model)
        else:
            # Entidad existente: buscar o crear modelo y actualizar
            result = await self.session.execute(
                select(OficinaORM).where(OficinaORM.id_oficina == oficina.id)
            )
            existing_orm = result.scalar_one_or_none()
            model = oficina_to_orm(oficina, existing_orm)
            if existing_orm is None:
                self.session.add(model)
        
        await self.session.flush()
        await self.session.refresh(model)
        
        return oficina_to_domain(model)
    
    async def create(self, oficina: Oficina) -> Oficina:
        """Crea una nueva oficina (alias para compatibilidad)"""
        return await self.save(oficina)
    
    async def update(self, oficina: Oficina) -> Oficina:
        """Actualiza una oficina existente (alias para compatibilidad)"""
        if oficina.id is None:
            raise ValueError("No se puede actualizar una oficina sin ID")
        return await self.save(oficina)
    
    async def delete(self, id: int) -> bool:
        """Elimina una oficina"""
        await self.session.execute(
            sql_delete(OficinaORM).where(OficinaORM.id_oficina == id)
        )
        return True

