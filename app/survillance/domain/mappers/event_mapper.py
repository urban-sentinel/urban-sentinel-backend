"""
Mapper for Event: conversion between domain entity and ORM model.
"""
from typing import Optional
from decimal import Decimal

from app.survillance.models.event_model import Evento as EventoORM
from app.survillance.domain.entities.event import Evento
from app.survillance.domain.enums import TipoEvento
from app.survillance.domain.value_objects.timestamps import DurationSeconds, MilliSeconds
from app.survillance.domain.value_objects.media_paths import SubclipPath
from ._helpers import _as_dt


def evento_to_domain(orm: EventoORM) -> Evento:
    """Converts ORM model to domain entity"""
    return Evento(
        id_conexion=orm.id_conexion,
        tipo_evento=TipoEvento(orm.tipo_evento),
        t_inicio_ms=MilliSeconds(orm.t_inicio_ms) if orm.t_inicio_ms is not None else MilliSeconds(0),
        t_fin_ms=MilliSeconds(orm.t_fin_ms) if orm.t_fin_ms is not None else MilliSeconds(0),
        timestamp_evento=orm.timestamp_evento,  # ORM already returns datetime with tz
        procesado=orm.procesado,
        id_clip=orm.id_clip,
        id_usuario=orm.id_usuario,
        confianza=float(orm.confianza) if orm.confianza else None,
        subclip_path=SubclipPath(orm.subclip_path) if orm.subclip_path else None,
        subclip_duracion_sec=DurationSeconds(orm.subclip_duracion_sec) if orm.subclip_duracion_sec is not None else None,
        id=orm.id_evento
    )


def evento_to_orm(entity: Evento, existing: Optional[EventoORM] = None) -> EventoORM:
    """Converts domain entity to ORM model"""
    orm = existing or EventoORM()
    
    # DO NOT set id_evento if entity.id is None (autoincrement)
    if entity.id is not None:
        orm.id_evento = entity.id
    
    orm.id_conexion = entity.id_conexion
    orm.tipo_evento = entity.tipo_evento.value
    orm.t_inicio_ms = int(entity.t_inicio_ms)
    orm.t_fin_ms = int(entity.t_fin_ms)
    orm.timestamp_evento = _as_dt(entity.timestamp_evento)
    orm.procesado = entity.procesado
    orm.id_clip = entity.id_clip
    orm.id_usuario = entity.id_usuario
    orm.confianza = Decimal(str(entity.confianza)) if entity.confianza is not None else None
    orm.subclip_path = str(entity.subclip_path) if entity.subclip_path else None
    orm.subclip_duracion_sec = int(entity.subclip_duracion_sec) if entity.subclip_duracion_sec is not None else None
    
    return orm

