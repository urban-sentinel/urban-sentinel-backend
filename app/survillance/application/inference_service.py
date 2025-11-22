"""
Servicio para procesar webhooks de inferencia (contratos A y B).
"""
from datetime import datetime, timedelta
from decimal import Decimal
from typing import List, Union

from fastapi import HTTPException, status

from app.shared.time import parse_utc, now_utc
from app.survillance.domain.entities import Evento, InferenceRequest
from app.survillance.domain.repositories_interfaces import *
from app.survillance.application.dto import *
from app.survillance.application.clip_resolver import ClipResolver


class InferenceService:
    """Servicio para procesar resultados de inferencia de IA"""
    
    def __init__(
        self,
        evento_repo: IEventoRepository,
        clip_repo: IClipRepository,
        inference_repo: IInferenceRequestRepository
    ):
        self.evento_repo = evento_repo
        self.clip_repo = clip_repo
        self.inference_repo = inference_repo
    
    async def process_webhook_a(
        self,
        data: InferenceWebhookRequestA
    ) -> InferenceWebhookResponse:
        """
        Procesa webhook con contrato A (offsets relativos al clip).
        
        Args:
            data: Datos del webhook con clip_id y offsets relativos
        
        Returns:
            Response con IDs de eventos creados
        """
        # Verificar idempotencia
        if await self.inference_repo.exists(data.request_id):
            return InferenceWebhookResponse(
                ok=True,
                created_event_ids=[],
                message="Request ya procesado (idempotente)"
            )
        
        # Registrar request
        inference_req = InferenceRequest(
            request_id=data.request_id,
            received_at=now_utc()
        )
        await self.inference_repo.create(inference_req)
        
        # Obtener clip
        if data.clip_id:
            clip = await self.clip_repo.get_by_id(data.clip_id)
        elif data.clip_path:
            # Buscar por path (simplificado, en producción usar índice)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Búsqueda por clip_path no implementada, usar clip_id"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Debe proveer clip_id o clip_path"
            )
        
        if not clip:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Clip no encontrado"
            )
        
        # Crear eventos
        created_ids = []
        
        for ev_data in data.eventos:
            # Calcular timestamp absoluto
            timestamp_evento = ClipResolver.calculate_absolute_timestamp(
                clip,
                ev_data.t_inicio_ms
            )
            
            evento = Evento(
                id_conexion=data.conexion_id,
                id_clip=clip.id_clip,
                tipo_evento=ev_data.tipo,
                confianza=Decimal(str(ev_data.confianza)),
                t_inicio_ms=ev_data.t_inicio_ms,
                t_fin_ms=ev_data.t_fin_ms,
                timestamp_evento=timestamp_evento,
                procesado=False
            )
            
            evento = await self.evento_repo.create(evento)
            created_ids.append(evento.id_evento)
        
        return InferenceWebhookResponse(
            ok=True,
            created_event_ids=created_ids
        )
    
    async def process_webhook_b(
        self,
        data: InferenceWebhookRequestB
    ) -> InferenceWebhookResponse:
        """
        Procesa webhook con contrato B (timestamps absolutos).
        
        Args:
            data: Datos del webhook con timestamps UTC absolutos
        
        Returns:
            Response con IDs de eventos creados
        """
        # Verificar idempotencia
        if await self.inference_repo.exists(data.request_id):
            return InferenceWebhookResponse(
                ok=True,
                created_event_ids=[],
                message="Request ya procesado (idempotente)"
            )
        
        # Registrar request
        inference_req = InferenceRequest(
            request_id=data.request_id,
            received_at=now_utc()
        )
        await self.inference_repo.create(inference_req)
        
        # Crear eventos
        created_ids = []
        
        for ev_data in data.eventos:
            # Parsear timestamp
            timestamp_evento = parse_utc(ev_data.timestamp_utc)
            end_time = timestamp_evento + timedelta(milliseconds=ev_data.dur_ms)
            
            # Buscar clips que cubren este rango
            clips = await self.clip_repo.get_by_time_range(
                data.conexion_id,
                timestamp_evento,
                end_time
            )
            
            # Usar el primer clip que intersecta (simplificado)
            clip = clips[0] if clips else None
            
            # Calcular offsets relativos si hay clip
            if clip:
                t_inicio_ms = ClipResolver.calculate_relative_offset(
                    clip,
                    timestamp_evento
                )
                t_fin_ms = t_inicio_ms + ev_data.dur_ms
            else:
                t_inicio_ms = None
                t_fin_ms = None
            
            evento = Evento(
                id_conexion=data.conexion_id,
                id_clip=clip.id_clip if clip else None,
                tipo_evento=ev_data.tipo,
                confianza=Decimal(str(ev_data.confianza)),
                t_inicio_ms=t_inicio_ms,
                t_fin_ms=t_fin_ms,
                timestamp_evento=timestamp_evento,
                procesado=False
            )
            
            evento = await self.evento_repo.create(evento)
            created_ids.append(evento.id_evento)
        
        return InferenceWebhookResponse(
            ok=True,
            created_event_ids=created_ids
        )
    
    async def process_webhook(
        self,
        payload: dict
    ) -> InferenceWebhookResponse:
        """
        Detecta automáticamente el contrato (A o B) y procesa el webhook.
        
        Args:
            payload: Diccionario con datos del webhook
        
        Returns:
            Response con IDs de eventos creados
        """
        # Detectar contrato por presencia de campos
        if "eventos" in payload and len(payload["eventos"]) > 0:
            primer_evento = payload["eventos"][0]
            
            # Contrato A: tiene t_inicio_ms
            if "t_inicio_ms" in primer_evento:
                data = InferenceWebhookRequestA(**payload)
                return await self.process_webhook_a(data)
            
            # Contrato B: tiene timestamp_utc
            elif "timestamp_utc" in primer_evento:
                data = InferenceWebhookRequestB(**payload)
                return await self.process_webhook_b(data)
        
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Formato de webhook inválido (no coincide con contrato A o B)"
        )