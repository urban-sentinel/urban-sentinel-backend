"""
Interfaz de repositorio de Reporte usando typing.Protocol.
"""
from typing import Protocol, Sequence, Optional

from ..entities.report import Reporte
from ..value_objects.identifiers import IdReporte, IdUsuario


class IReporteRepository(Protocol):
    """Repositorio de reportes"""
    
    async def get(self, id: IdReporte) -> Optional[Reporte]:
        """Obtiene un reporte por ID"""
        ...
    
    async def list(
        self,
        limit: int = 50,
        offset: int = 0,
        id_usuario: Optional[IdUsuario] = None
    ) -> Sequence[Reporte]:
        """Lista reportes con filtros opcionales"""
        ...
    
    async def create(self, reporte: Reporte) -> Reporte:
        """Crea un nuevo reporte"""
        ...


