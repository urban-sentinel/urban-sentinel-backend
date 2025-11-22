"""
Interfaces de repositorios de dominio: exportaciones centralizadas.
"""
from .oficina_repository_interface import IOficinaRepository
from .conexion_repository_interface import IConexionRepository
from .clip_repository_interface import IClipRepository
from .usuario_repository_interface import IUsuarioRepository
from .evento_repository_interface import IEventoRepository
from .notificacion_repository_interface import INotificacionRepository
from .reporte_repository_interface import IReporteRepository
from .inference_request_repository_interface import IInferenceRequestRepository
from .event_snapshot_repository_interface import IEventSnapshotRepository

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



