"""
Mapper for Clip: conversion between domain entity and ORM model.
"""
from typing import Optional

from app.survillance.models.clip_model import Clip as ClipORM
from app.survillance.domain.entities.clip import Clip
from app.survillance.domain.value_objects.timestamps import DurationSeconds
from app.survillance.domain.value_objects.media_paths import StoragePath
from ._helpers import _as_dt


def clip_to_domain(orm: ClipORM) -> Clip:
    """Converts ORM model to domain entity"""
    return Clip(
        id_conexion=orm.id_conexion,
        storage_path=StoragePath(orm.storage_path),
        start_time_utc=orm.start_time_utc,  # ORM already returns datetime with tz
        duration_sec=DurationSeconds(orm.duration_sec),
        fecha_guardado=orm.fecha_guardado,  # ORM already returns datetime with tz
        id=orm.id_clip
    )


def clip_to_orm(entity: Clip, existing: Optional[ClipORM] = None) -> ClipORM:
    """Converts domain entity to ORM model"""
    orm = existing or ClipORM()
    
    # DO NOT set id_clip if entity.id is None (autoincrement)
    if entity.id is not None:
        orm.id_clip = entity.id
    
    orm.id_conexion = entity.id_conexion
    orm.storage_path = str(entity.storage_path)
    orm.start_time_utc = _as_dt(entity.start_time_utc)
    orm.duration_sec = int(entity.duration_sec)
    # fecha_guardado: if None, ORM will use default (now_utc)
    if entity.fecha_guardado is not None:
        orm.fecha_guardado = _as_dt(entity.fecha_guardado)
    
    return orm

