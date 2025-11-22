"""
Interfaz de repositorio de Oficina usando typing.Protocol.
"""
from typing import Protocol, Sequence, Optional

from ..entities.office import Oficina
from ..value_objects.identifiers import IdOficina


class IOficinaRepository(Protocol):
    """Repositorio de oficinas"""
    
    async def get(self, id: IdOficina) -> Optional[Oficina]:
        """Obtiene una oficina por ID"""
        ...
    
    async def list(self, limit: int = 50, offset: int = 0) -> Sequence[Oficina]:
        """Lista oficinas con paginación"""
        ...
    
    async def create(self, oficina: Oficina) -> Oficina:
        """Crea una nueva oficina"""
        ...
    
    async def update(self, oficina: Oficina) -> Oficina:
        """Actualiza una oficina existente"""
        ...
    
    async def delete(self, id: IdOficina) -> None:
        """Elimina una oficina"""
        ...


