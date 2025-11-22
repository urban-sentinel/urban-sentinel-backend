"""
Interfaz de repositorio de Clip usando typing.Protocol.
"""
from typing import Protocol, Sequence, Optional

from ..entities.clip import Clip
from ..value_objects.identifiers import IdClip, IdConexion
from ..value_objects.timestamps import UtcDatetime


class IClipRepository(Protocol):
    """Repositorio de clips"""
    
    async def get(self, id: IdClip) -> Optional[Clip]:
        """Obtiene un clip por ID"""
        ...
    
    async def list(
        self,
        limit: int = 50,
        offset: int = 0,
        id_conexion: Optional[IdConexion] = None,
        start_time: Optional[UtcDatetime] = None,
        end_time: Optional[UtcDatetime] = None
    ) -> Sequence[Clip]:
        """Lista clips con filtros opcionales"""
        ...
    
    async def find_by_time_range(
        self,
        id_conexion: IdConexion,
        start_time: UtcDatetime,
        end_time: UtcDatetime
    ) -> Sequence[Clip]:
        """Encuentra clips que intersectan con un rango de tiempo"""
        ...
    
    async def find_old_clips(
        self,
        id_conexion: IdConexion,
        older_than: UtcDatetime
    ) -> Sequence[Clip]:
        """Encuentra clips más antiguos que una fecha"""
        ...
    
    async def create(self, clip: Clip) -> Clip:
        """Crea un nuevo clip"""
        ...
    
    async def delete(self, id: IdClip) -> None:
        """Elimina un clip"""
        ...



