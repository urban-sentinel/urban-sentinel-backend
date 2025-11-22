"""
Repositorios: reexportaciones para compatibilidad.
Los repositorios están ahora en .repositories/
"""
from .repositories import (
    OficinaRepository,
    ConexionRepository,
    ClipRepository,
    UsuarioRepository,
    EventoRepository,
    NotificacionRepository,
    ReporteRepository,
    InferenceRequestRepository,
)

__all__ = [
    "OficinaRepository",
    "ConexionRepository",
    "ClipRepository",
    "UsuarioRepository",
    "EventoRepository",
    "NotificacionRepository",
    "ReporteRepository",
    "InferenceRequestRepository",
]
