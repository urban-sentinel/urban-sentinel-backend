"""
Mapper for Office: conversion between domain entity and ORM model.
"""
from typing import Optional

from app.survillance.models.office_model import Oficina as OficinaORM
from app.survillance.domain.entities.office import Oficina
from ._helpers import _as_dt


def oficina_to_domain(orm: OficinaORM) -> Oficina:
    """Converts ORM model to domain entity"""
    return Oficina(
        nombre_oficina=orm.nombre_oficina,
        direccion=orm.direccion,
        ciudad=orm.ciudad,
        responsable=orm.responsable,
        telefono_contacto=orm.telefono_contacto,
        fecha_registro=orm.fecha_registro,  # ORM already returns datetime with tz
        id=orm.id_oficina
    )


def oficina_to_orm(entity: Oficina, existing: Optional[OficinaORM] = None) -> OficinaORM:
    """Converts domain entity to ORM model"""
    orm = existing or OficinaORM()
    
    # DO NOT set id_oficina if entity.id is None (autoincrement)
    if entity.id is not None:
        orm.id_oficina = entity.id
    
    orm.nombre_oficina = entity.nombre_oficina
    orm.direccion = entity.direccion
    orm.ciudad = entity.ciudad
    orm.responsable = entity.responsable
    orm.telefono_contacto = entity.telefono_contacto
    # fecha_registro: if None, ORM will use default (now_utc)
    if entity.fecha_registro is not None:
        orm.fecha_registro = _as_dt(entity.fecha_registro)
    
    return orm

