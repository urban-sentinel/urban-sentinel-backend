"""
Interfaz de repositorio de Usuario usando typing.Protocol.
"""
from typing import Protocol, Optional

from ..entities.user import Usuario
from ..value_objects.identifiers import IdUsuario


class IUsuarioRepository(Protocol):
    """Repositorio de usuarios"""
    
    async def get(self, id: IdUsuario) -> Optional[Usuario]:
        """Obtiene un usuario por ID"""
        ...
    
    async def get_by_email(self, email: str) -> Optional[Usuario]:
        """Obtiene un usuario por email"""
        ...
    
    async def create(self, usuario: Usuario) -> Usuario:
        """Crea un nuevo usuario"""
        ...
    
    async def update(self, usuario: Usuario) -> Usuario:
        """Actualiza un usuario existente"""
        ...


