"""
Interfaz de repositorio de EventSnapshot usando typing.Protocol.
"""
from typing import Protocol, Sequence, Optional

from ..entities.event_snapshot import EventSnapshot
from ..value_objects.identifiers import IdEventSnapshot, IdEvento


class IEventSnapshotRepository(Protocol):
    """Repositorio de event snapshots"""
    
    async def get(self, id: IdEventSnapshot) -> Optional[EventSnapshot]:
        """Obtiene un snapshot por ID"""
        ...
    
    async def list_by_event(
        self,
        id_evento: IdEvento,
        limit: int = 50,
        offset: int = 0
    ) -> Sequence[EventSnapshot]:
        """Lista snapshots de un evento específico"""
        ...
    
    async def create(self, snapshot: EventSnapshot) -> EventSnapshot:
        """Crea un nuevo snapshot"""
        ...
    
    async def delete(self, id: IdEventSnapshot) -> None:
        """Elimina un snapshot"""
        ...



