"""
Repositorio de Usuario: implementación con SQLAlchemy.
"""
from typing import Optional

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.survillance.models import Usuario as UsuarioORM
from app.survillance.domain.entities.user import Usuario
from app.survillance.domain.mappers import usuario_to_domain, usuario_to_orm


class UsuarioRepository:
    """Adaptador de repositorio de usuarios usando entidades de dominio"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get(self, id: int) -> Optional[Usuario]:
        """Obtiene un usuario por ID"""
        result = await self.session.execute(
            select(UsuarioORM).where(UsuarioORM.id_usuario == id)
        )
        orm = result.scalar_one_or_none()
        return usuario_to_domain(orm) if orm else None
    
    async def get_all(self) -> list[Usuario]:
        """Obtiene todos los usuarios"""
        result = await self.session.execute(
            select(UsuarioORM)
        )
        orms = result.scalars().all()
        return [usuario_to_domain(orm) for orm in orms]
    
    async def get_by_id(self, id: int) -> Optional[Usuario]:
        """Obtiene un usuario por ID (alias para servicios)"""
        return await self.get(id)
    
    async def get_by_email(self, email: str) -> Optional[Usuario]:
        """Obtiene un usuario por email"""
        result = await self.session.execute(
            select(UsuarioORM).where(UsuarioORM.email == email)
        )
        orm = result.scalar_one_or_none()
        return usuario_to_domain(orm) if orm else None
    
    async def delete_by_id(self, id: int) -> None:
        """Elimina un usuario por ID"""
        await self.session.execute(
            delete(UsuarioORM).where(UsuarioORM.id_usuario == id)
        )
        await self.session.flush()

    async def save(self, usuario: Usuario) -> Usuario:
        """
        Guarda un usuario (crea o actualiza según si tiene ID).
        Si entity.id is None: crea nuevo registro.
        Si entity.id is not None: actualiza registro existente.
        """
        if usuario.id is None:
            # Nueva entidad: crear modelo sin ID
            model = usuario_to_orm(usuario)
            self.session.add(model)
        else:
            # Entidad existente: buscar o crear modelo y actualizar
            result = await self.session.execute(
                select(UsuarioORM).where(UsuarioORM.id_usuario == usuario.id)
            )
            existing_orm = result.scalar_one_or_none()
            model = usuario_to_orm(usuario, existing_orm)
            if existing_orm is None:
                self.session.add(model)
        
        await self.session.flush()
        await self.session.refresh(model)
        
        return usuario_to_domain(model)
    
    async def create(self, usuario: Usuario) -> Usuario:
        """Crea un nuevo usuario (alias para compatibilidad)"""
        return await self.save(usuario)
    
    async def update(self, usuario: Usuario) -> Usuario:
        """Actualiza un usuario existente (alias para compatibilidad)"""
        if usuario.id is None:
            raise ValueError("No se puede actualizar un usuario sin ID")
        return await self.save(usuario)


