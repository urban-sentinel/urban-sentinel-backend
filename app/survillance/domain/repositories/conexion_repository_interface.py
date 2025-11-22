"""
Interfaz de repositorio de Conexion usando typing.Protocol.
"""
from typing import Protocol, Sequence, Optional

from ..entities.connection import Conexion
from ..value_objects.identifiers import IdOficina, IdConexion


class IConexionRepository(Protocol):
    """Repositorio de conexiones/cámaras"""
    
    async def get(self, id: IdConexion) -> Optional[Conexion]:
        """Obtiene una conexión por ID"""
        ...
    
    async def list(
        self,
        limit: int = 50,
        offset: int = 0,
        id_oficina: Optional[IdOficina] = None,
        habilitada: Optional[bool] = None
    ) -> Sequence[Conexion]:
        """Lista conexiones con filtros opcionales"""
        ...
    
    async def list_enabled(self) -> Sequence[Conexion]:
        """Lista solo conexiones habilitadas"""
        ...
    
    async def create(self, conexion: Conexion) -> Conexion:
        """Crea una nueva conexión"""
        ...
    
    async def update(self, conexion: Conexion) -> Conexion:
        """Actualiza una conexión existente"""
        ...
    
    async def delete(self, id: IdConexion) -> None:
        """Elimina una conexión"""
        ...


