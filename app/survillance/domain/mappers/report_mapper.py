"""
Mapper for Report: conversion between domain entity and ORM model.
"""
from typing import Optional
from decimal import Decimal

from app.survillance.models.report_model import Reporte as ReporteORM
from app.survillance.domain.entities.report import Reporte
from ._helpers import _as_dt


def reporte_to_domain(orm: ReporteORM) -> Reporte:
    """Converts ORM model to domain entity"""
    return Reporte(
        id_usuario=orm.id_usuario,
        titulo=orm.titulo or "",
        descripcion=orm.descripcion,
        id_clip=orm.id_clip,
        rango_fecha_inicio=orm.rango_fecha_inicio,  # ORM already returns datetime with tz or None
        rango_fecha_fin=orm.rango_fecha_fin,  # ORM already returns datetime with tz or None
        filtro_confianza=float(orm.filtro_confianza) if orm.filtro_confianza else None,
        tipo_evento=orm.tipo_evento,
        fecha_generacion=orm.fecha_generacion,  # ORM already returns datetime with tz
        id=orm.id_reporte
    )


def reporte_to_orm(entity: Reporte, existing: Optional[ReporteORM] = None) -> ReporteORM:
    """Converts domain entity to ORM model"""
    orm = existing or ReporteORM()
    
    # DO NOT set id_reporte if entity.id is None (autoincrement)
    if entity.id is not None:
        orm.id_reporte = entity.id
    
    orm.id_usuario = entity.id_usuario
    orm.titulo = entity.titulo
    orm.descripcion = entity.descripcion
    orm.id_clip = entity.id_clip
    # fecha_generacion: if None, ORM will use default (now_utc)
    if entity.fecha_generacion is not None:
        orm.fecha_generacion = _as_dt(entity.fecha_generacion)
    if entity.rango_fecha_inicio is not None:
        orm.rango_fecha_inicio = _as_dt(entity.rango_fecha_inicio)
    if entity.rango_fecha_fin is not None:
        orm.rango_fecha_fin = _as_dt(entity.rango_fecha_fin)
    orm.filtro_confianza = Decimal(str(entity.filtro_confianza)) if entity.filtro_confianza is not None else None
    orm.tipo_evento = entity.tipo_evento
    
    return orm

