"""
Mapper for Connection: conversion between domain entity and ORM model.
"""
from typing import Optional

from app.survillance.models.connection_model import Conexion as ConexionORM
from app.survillance.domain.entities.connection import Conexion
from app.survillance.domain.enums import ModoIngesta
from ._helpers import _as_dt


def conexion_to_domain(orm: ConexionORM) -> Conexion:
    """Converts ORM model to domain entity"""
    return Conexion(
        id_oficina=orm.id_oficina,
        nombre_camara=orm.nombre_camara,
        rtsp_url=orm.rtsp_url,
        modo_ingesta=ModoIngesta(orm.modo_ingesta),
        habilitada=orm.habilitada,
        retention_minutes=orm.retention_minutes,
        ubicacion=orm.ubicacion,
        estado=orm.estado,
        ultimo_ping=orm.ultimo_ping,  # ORM already returns datetime with tz or None
        fps_sample=orm.fps_sample,
        created_at=orm.created_at,  # ORM already returns datetime with tz
        updated_at=orm.updated_at,  # Can be None
        id=orm.id_conexion
    )


def conexion_to_orm(entity: Conexion, existing: Optional[ConexionORM] = None) -> ConexionORM:
    """Converts domain entity to ORM model"""
    orm = existing or ConexionORM()
    
    # DO NOT set id_conexion if entity.id is None (autoincrement)
    if entity.id is not None:
        orm.id_conexion = entity.id
    
    orm.id_oficina = entity.id_oficina
    orm.nombre_camara = entity.nombre_camara
    orm.rtsp_url = entity.rtsp_url
    orm.modo_ingesta = entity.modo_ingesta.value
    orm.habilitada = entity.habilitada
    orm.retention_minutes = entity.retention_minutes
    orm.ubicacion = entity.ubicacion
    orm.estado = entity.estado
    # created_at: if None, ORM will use default (now_utc)
    if entity.created_at is not None:
        orm.created_at = _as_dt(entity.created_at)
    if entity.ultimo_ping is not None:
        orm.ultimo_ping = _as_dt(entity.ultimo_ping)
    orm.fps_sample = entity.fps_sample
    if entity.updated_at is not None:
        orm.updated_at = _as_dt(entity.updated_at)
    
    return orm

