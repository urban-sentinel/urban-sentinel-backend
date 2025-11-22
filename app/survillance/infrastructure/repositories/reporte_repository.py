"""
Repositorio de Reporte: implementación con SQLAlchemy.
"""
from typing import Optional, Sequence, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.survillance.models import Reporte as ReporteORM
from app.survillance.domain.entities.report import Reporte
from app.survillance.domain.mappers import reporte_to_domain, reporte_to_orm


class ReporteRepository:
    """Adaptador de repositorio de reportes usando entidades de dominio"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get(self, id: int) -> Optional[Reporte]:
        """Obtiene un reporte por ID"""
        result = await self.session.execute(
            select(ReporteORM).where(ReporteORM.id_reporte == id)
        )
        orm = result.scalar_one_or_none()
        return reporte_to_domain(orm) if orm else None
    
    async def get_by_id(self, id: int) -> Optional[Reporte]:
        """Obtiene un reporte por ID (alias para servicios)"""
        return await self.get(id)
    
    async def list(
        self,
        limit: int = 50,
        offset: int = 0,
        id_usuario: Optional[int] = None
    ) -> Sequence[Reporte]:
        """Lista reportes con filtros opcionales"""
        query = select(ReporteORM)
        
        if id_usuario is not None:
            query = query.where(ReporteORM.id_usuario == id_usuario)
        
        query = query.order_by(ReporteORM.fecha_generacion.desc()).limit(limit).offset(offset)
        result = await self.session.execute(query)
        return [reporte_to_domain(orm) for orm in result.scalars().all()]
    
    async def get_all(
        self,
        limit: int = 100,
        offset: int = 0,
        id_usuario: Optional[int] = None
    ) -> List[Reporte]:
        """Lista todos los reportes con filtros (alias para servicios)"""
        return list(await self.list(limit, offset, id_usuario))
    
    async def save(self, reporte: Reporte) -> Reporte:
        """
        Guarda un reporte (crea o actualiza según si tiene ID).
        Si entity.id is None: crea nuevo registro.
        Si entity.id is not None: actualiza registro existente.
        """
        if reporte.id is None:
            # Nueva entidad: crear modelo sin ID
            model = reporte_to_orm(reporte)
            self.session.add(model)
        else:
            # Entidad existente: buscar o crear modelo y actualizar
            result = await self.session.execute(
                select(ReporteORM).where(ReporteORM.id_reporte == reporte.id)
            )
            existing_orm = result.scalar_one_or_none()
            model = reporte_to_orm(reporte, existing_orm)
            if existing_orm is None:
                self.session.add(model)
        
        await self.session.flush()
        await self.session.refresh(model)
        
        return reporte_to_domain(model)
    
    async def create(self, reporte: Reporte) -> Reporte:
        """Crea un nuevo reporte (alias para compatibilidad)"""
        return await self.save(reporte)


