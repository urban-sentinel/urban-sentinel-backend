"""
Mapper for User: conversion between domain entity and ORM model.
"""
from typing import Optional

from app.survillance.models.user_model import Usuario as UsuarioORM
from app.survillance.domain.entities.user import Usuario
from ._helpers import _as_dt


def usuario_to_domain(orm: UsuarioORM) -> Usuario:
    """Converts ORM model to domain entity"""
    return Usuario(
        nombre=orm.nombre,
        email=orm.email,
        password_hash=orm.password_hash,
        apellido=orm.apellido,
        rol=orm.rol,
        phone=orm.phone,
        fecha_creacion=orm.fecha_creacion,  # ORM already returns datetime with tz
        ultimo_login=orm.ultimo_login,  # Can be None
        id=orm.id_usuario
    )


def usuario_to_orm(entity: Usuario, existing: Optional[UsuarioORM] = None) -> UsuarioORM:
    """Converts domain entity to ORM model"""
    orm = existing or UsuarioORM()
    
    # DO NOT set id_usuario if entity.id is None (autoincrement)
    if entity.id is not None:
        orm.id_usuario = entity.id
    
    orm.nombre = entity.nombre
    orm.apellido = entity.apellido
    orm.email = entity.email
    orm.password_hash = entity.password_hash
    orm.rol = entity.rol
    orm.phone = entity.phone
    # fecha_creacion: if None, ORM will use default (now_utc)
    if entity.fecha_creacion is not None:
        orm.fecha_creacion = _as_dt(entity.fecha_creacion)
    # ultimo_login can be None
    if entity.ultimo_login is not None:
        orm.ultimo_login = _as_dt(entity.ultimo_login)
    
    return orm

