"""
Repositorio de Conexion: implementación con SQLAlchemy.
"""
from typing import Optional, Sequence, List

from sqlalchemy import select, delete as sql_delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.survillance.models import Conexion as ConexionORM
from app.survillance.domain.entities.connection import Conexion
from app.survillance.domain.mappers import conexion_to_domain, conexion_to_orm


class ConexionRepository:
    """Adaptador de repositorio de conexiones usando entidades de dominio"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get(self, id: int) -> Optional[Conexion]:
        """Obtiene una conexión por ID"""
        result = await self.session.execute(
            select(ConexionORM).where(ConexionORM.id_conexion == id)
        )
        orm = result.scalar_one_or_none()
        return conexion_to_domain(orm) if orm else None
    
    async def get_by_id(self, id: int) -> Optional[Conexion]:
        """Obtiene una conexión por ID (alias para servicios)"""
        return await self.get(id)
    
    async def list(
        self,
        limit: int = 50,
        offset: int = 0,
        id_oficina: Optional[int] = None,
        habilitada: Optional[bool] = None
    ) -> Sequence[Conexion]:
        """Lista conexiones con filtros opcionales"""
        query = select(ConexionORM)
        
        if id_oficina is not None:
            query = query.where(ConexionORM.id_oficina == id_oficina)
        
        if habilitada is not None:
            query = query.where(ConexionORM.habilitada == habilitada)
        
        query = query.limit(limit).offset(offset)
        result = await self.session.execute(query)
        return [conexion_to_domain(orm) for orm in result.scalars().all()]
    
    async def get_all(
        self,
        limit: int = 100,
        offset: int = 0,
        id_oficina: Optional[int] = None,
        habilitada: Optional[bool] = None
    ) -> List[Conexion]:
        """Lista todas las conexiones con filtros (alias para servicios)"""
        return list(await self.list(limit, offset, id_oficina, habilitada))
    
    async def list_enabled(self) -> Sequence[Conexion]:
        """Lista solo conexiones habilitadas"""
        result = await self.session.execute(
            select(ConexionORM).where(ConexionORM.habilitada == True)
        )
        return [conexion_to_domain(orm) for orm in result.scalars().all()]
    
    async def save(self, conexion: Conexion) -> Conexion:
        """
        Guarda una conexión (crea o actualiza según si tiene ID).
        Si entity.id is None: crea nuevo registro.
        Si entity.id is not None: actualiza registro existente.
        """
        if conexion.id is None:
            # Nueva entidad: crear modelo sin ID
            model = conexion_to_orm(conexion)
            self.session.add(model)
        else:
            # Entidad existente: buscar o crear modelo y actualizar
            result = await self.session.execute(
                select(ConexionORM).where(ConexionORM.id_conexion == conexion.id)
            )
            existing_orm = result.scalar_one_or_none()
            model = conexion_to_orm(conexion, existing_orm)
            if existing_orm is None:
                self.session.add(model)
        
        await self.session.flush()
        await self.session.refresh(model)
        
        return conexion_to_domain(model)
    
    async def create(self, conexion: Conexion) -> Conexion:
        """Crea una nueva conexión (alias para compatibilidad)"""
        return await self.save(conexion)
    
    async def update(self, conexion: Conexion) -> Conexion:
        """Actualiza una conexión existente (alias para compatibilidad)"""
        if conexion.id is None:
            raise ValueError("No se puede actualizar una conexión sin ID")
        return await self.save(conexion)
    
    async def delete(self, id: int) -> bool:
        """Elimina una conexión"""
        await self.session.execute(
            sql_delete(ConexionORM).where(ConexionORM.id_conexion == id)
        )
        return True

