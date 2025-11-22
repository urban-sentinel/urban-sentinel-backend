"""
Domain enums: event types, ingestion modes, states.
"""
from enum import Enum


class TipoEvento(str, Enum):
    """Detectable security event types"""
    FORCEJEO = "forcejeo"
    PATADA = "patada"
    GOLPE = "golpe"


class ModoIngesta(str, Enum):
    """Video ingestion modes"""
    WEBHOOK_ONLY = "WEBHOOK_ONLY"
    PUSH = "PUSH"
    SEGMENT = "SEGMENT"


class EstadoConexion(str, Enum):
    """Possible connection states"""
    ACTIVA = "activa"
    INACTIVA = "inactiva"
    ERROR = "error"


class EstadoNotificacion(str, Enum):
    """Notification states"""
    PENDIENTE = "pendiente"
    ENVIADA = "enviada"
    FALLIDA = "fallida"