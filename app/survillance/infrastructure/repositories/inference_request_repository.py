"""
Repositorio de InferenceRequest: implementación con SQLAlchemy.
"""
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.survillance.models import InferenceRequest as InferenceRequestORM
from app.survillance.domain.entities.inference_request import InferenceRequest
from app.survillance.domain.mappers import inference_request_to_domain, inference_request_to_orm


class InferenceRequestRepository:
    """Adaptador de repositorio de inference requests usando entidades de dominio"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get(self, id: int) -> Optional[InferenceRequest]:
        """Obtiene un inference request por ID"""
        result = await self.session.execute(
            select(InferenceRequestORM).where(InferenceRequestORM.id == id)
        )
        orm = result.scalar_one_or_none()
        return inference_request_to_domain(orm) if orm else None
    
    async def get_by_id(self, id: int) -> Optional[InferenceRequest]:
        """Obtiene un inference request por ID (alias para servicios)"""
        return await self.get(id)
    
    async def get_by_request_id(self, request_id: str) -> Optional[InferenceRequest]:
        """Obtiene un inference request por request_id único"""
        result = await self.session.execute(
            select(InferenceRequestORM).where(InferenceRequestORM.request_id == request_id)
        )
        orm = result.scalar_one_or_none()
        return inference_request_to_domain(orm) if orm else None
    
    async def exists_by_request_id(self, request_id: str) -> bool:
        """Verifica si un request_id ya existe (idempotencia)"""
        result = await self.session.execute(
            select(InferenceRequestORM).where(InferenceRequestORM.request_id == request_id)
        )
        return result.scalar_one_or_none() is not None
    
    async def save(self, inference_request: InferenceRequest) -> InferenceRequest:
        """
        Guarda un inference request (crea o actualiza según si tiene ID).
        Si entity.id is None: crea nuevo registro.
        Si entity.id is not None: actualiza registro existente.
        """
        if inference_request.id is None:
            # Nueva entidad: crear modelo sin ID
            model = inference_request_to_orm(inference_request)
            self.session.add(model)
        else:
            # Entidad existente: buscar o crear modelo y actualizar
            result = await self.session.execute(
                select(InferenceRequestORM).where(InferenceRequestORM.id == inference_request.id)
            )
            existing_orm = result.scalar_one_or_none()
            model = inference_request_to_orm(inference_request, existing_orm)
            if existing_orm is None:
                self.session.add(model)
        
        await self.session.flush()
        await self.session.refresh(model)
        
        return inference_request_to_domain(model)
    
    async def create(self, inference_request: InferenceRequest) -> InferenceRequest:
        """Crea un nuevo inference request (alias para compatibilidad)"""
        return await self.save(inference_request)



