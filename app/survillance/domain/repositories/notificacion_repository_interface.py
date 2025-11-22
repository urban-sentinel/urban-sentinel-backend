"""
Interfaz de repositorio de Notificacion usando typing.Protocol.
"""
from typing import Protocol, Sequence, Optional

from ..entities.notification import Notificacion
from ..value_objects.identifiers import IdNotificacion, IdEvento


class INotificacionRepository(Protocol):
    """Repositorio de notificaciones"""
    
    async def get(self, id: IdNotificacion) -> Optional[Notificacion]:
        """Obtiene una notificación por ID"""
        ...
    
    async def list(
        self,
        limit: int = 50,
        offset: int = 0,
        id_evento: Optional[IdEvento] = None
    ) -> Sequence[Notificacion]:
        """Lista notificaciones con filtros opcionales"""
        ...
    
    async def create(self, notificacion: Notificacion) -> Notificacion:
        """Crea una nueva notificación"""
        ...
    
    async def update(self, notificacion: Notificacion) -> Notificacion:
        """Actualiza una notificación existente"""
        ...


