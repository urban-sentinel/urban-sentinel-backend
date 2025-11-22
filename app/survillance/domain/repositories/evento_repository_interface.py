"""
Interfaz de repositorio de Evento usando typing.Protocol.
"""
from typing import Protocol, Sequence, Optional

from ..entities.event import Evento
from ..value_objects.identifiers import IdEvento, IdConexion
from ..value_objects.timestamps import UtcDatetime


class IEventoRepository(Protocol):
    """Repositorio de eventos"""
    
    async def get(self, id: IdEvento) -> Optional[Evento]:
        """Obtiene un evento por ID"""
        ...
    
    async def list(
        self,
        limit: int = 50,
        offset: int = 0,
        id_conexion: Optional[IdConexion] = None,
        tipo_evento: Optional[str] = None,
        start_time: Optional[UtcDatetime] = None,
        end_time: Optional[UtcDatetime] = None
    ) -> Sequence[Evento]:
        """Lista eventos con filtros opcionales"""
        ...
    
    async def create(self, evento: Evento) -> Evento:
        """Crea un nuevo evento"""
        ...
    
    async def update(self, evento: Evento) -> Evento:
        """Actualiza un evento existente"""
        ...


