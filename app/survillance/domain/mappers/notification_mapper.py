"""
Mapper for Notification: conversion between domain entity and ORM model.
"""
from typing import Optional

from app.survillance.models.notification_model import Notificacion as NotificacionORM
from app.survillance.domain.entities.notification import Notificacion
from app.survillance.domain.enums import EstadoNotificacion
from ._helpers import _as_dt


def notificacion_to_domain(orm: NotificacionORM) -> Notificacion:
    """Converts ORM model to domain entity"""
    return Notificacion(
        mensaje=orm.mensaje or "",
        canal=orm.canal or "",
        destinatario=orm.destinatario or "",
        estado=EstadoNotificacion(orm.estado),
        fecha_envio=orm.fecha_envio,  # ORM already returns datetime with tz or None
        id=orm.id_notificacion
    )


def notificacion_to_orm(entity: Notificacion, existing: Optional[NotificacionORM] = None) -> NotificacionORM:
    """Converts domain entity to ORM model"""
    orm = existing or NotificacionORM()
    
    # DO NOT set id_notificacion if entity.id is None (autoincrement)
    if entity.id is not None:
        orm.id_notificacion = entity.id
    
    orm.mensaje = entity.mensaje
    orm.canal = entity.canal
    orm.destinatario = entity.destinatario
    orm.estado = entity.estado.value
    # fecha_envio can be None
    if entity.fecha_envio is not None:
        orm.fecha_envio = _as_dt(entity.fecha_envio)
    
    return orm

