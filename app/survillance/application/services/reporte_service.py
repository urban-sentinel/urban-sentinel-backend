"""
Servicio CRUD de reportes.
"""
from typing import List, Optional

from app.shared.time import now_utc
from app.survillance.domain.entities.report import Reporte
from app.survillance.domain.repositories_interfaces import IReporteRepository
from app.survillance.application.dto import ReporteCreate


class ReporteService:
    """Servicio CRUD de reportes"""
    
    def __init__(self, reporte_repo: IReporteRepository):
        self.reporte_repo = reporte_repo
    
    async def create(self, data: ReporteCreate, id_usuario: int) -> Reporte:
        """Crea un reporte"""
        reporte = Reporte(
            id_usuario=id_usuario,
            titulo=data.titulo,
            descripcion=data.descripcion,
            id_clip=data.id_clip,
            rango_fecha_inicio=data.rango_fecha_inicio,
            rango_fecha_fin=data.rango_fecha_fin,
            filtro_confianza=data.filtro_confianza,
            tipo_evento=data.tipo_evento,
            fecha_generacion=now_utc()
        )
        return await self.reporte_repo.create(reporte)
    
    async def get_all(
        self,
        limit: int = 100,
        offset: int = 0,
        id_usuario: Optional[int] = None
    ) -> List[Reporte]:
        """Lista reportes"""
        return await self.reporte_repo.get_all(limit, offset, id_usuario)

