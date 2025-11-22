"""
Interfaces de repositorios de dominio: reexportaciones para compatibilidad.
Las interfaces están ahora en .repositories/
"""
from .repositories import (
    IOficinaRepository,
    IConexionRepository,
    IClipRepository,
    IUsuarioRepository,
    IEventoRepository,
    INotificacionRepository,
    IReporteRepository,
    IInferenceRequestRepository,
    IEventSnapshotRepository,
)

__all__ = [
    "IOficinaRepository",
    "IConexionRepository",
    "IClipRepository",
    "IUsuarioRepository",
    "IEventoRepository",
    "INotificacionRepository",
    "IReporteRepository",
    "IInferenceRequestRepository",
    "IEventSnapshotRepository",
]
