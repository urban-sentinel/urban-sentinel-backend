"""
Servicio para gestión de eventos.
"""
from datetime import datetime, timedelta
from typing import List, Optional
import os

from fastapi import HTTPException, status

from app.survillance.domain.entities.event import Evento
from app.survillance.domain.repositories_interfaces import IEventoRepository, IClipRepository
from app.survillance.application.clip_resolver import ClipResolver
from app.survillance.domain.value_objects.media_paths import SubclipPath
from app.survillance.domain.value_objects.timestamps import DurationSeconds
from app.config.settings import settings

from app.survillance.domain.value_objects.timestamps import MilliSeconds
from app.survillance.domain.enums import TipoEvento


class EventoService:
    """Servicio para gestión de eventos"""
    
    def __init__(
        self,
        evento_repo: IEventoRepository,
        clip_repo: IClipRepository
    ):
        self.evento_repo = evento_repo
        self.clip_repo = clip_repo

    async def create_evento(
        self,
        *,
        id_conexion: int,
        id_clip: int,
        tipo_evento: TipoEvento,
        confianza: Optional[float],
        t_inicio_ms: int,
        t_fin_ms: int,
        timestamp_evento: datetime,
        subclip_path: Optional[str] = None,
        subclip_duracion_sec: Optional[int] = None,
        procesado: bool = False,
    ) -> Evento:
        """
        Crea y persiste un Evento.
        """
        entity = Evento(
            id_conexion=id_conexion,
            id_clip=id_clip,
            tipo_evento=tipo_evento,
            confianza=confianza,
            t_inicio_ms=MilliSeconds(t_inicio_ms),
            t_fin_ms=MilliSeconds(t_fin_ms),
            timestamp_evento=timestamp_evento,
            subclip_path=SubclipPath(subclip_path) if subclip_path else None,
            subclip_duracion_sec=DurationSeconds(subclip_duracion_sec) if subclip_duracion_sec is not None else None,
            procesado=procesado,
        )
        return await self.evento_repo.create(entity)
    
    async def get_by_id(self, id_evento: int) -> Evento:
        """Obtiene evento por ID"""
        evento = await self.evento_repo.get_by_id(id_evento)
        if not evento:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Evento no encontrado"
            )
        return evento
    
    async def get_all(
        self,
        limit: int = 100,
        offset: int = 0,
        id_conexion: Optional[int] = None,
        tipo_evento: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> List[Evento]:
        """Lista eventos con filtros"""
        return await self.evento_repo.get_all(
            limit, offset, id_conexion, tipo_evento, start_time, end_time
        )
    
    async def generar_subclip(self, id_evento: int, padding: int = 2) -> Evento:
        """
        Genera un subclip del evento, concatenando múltiples clips si es necesario.
        """
        evento = await self.get_by_id(id_evento)
        # ... (resto queda igual)
