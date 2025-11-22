"""
Repositorios de dominio: exportaciones centralizadas.
"""
from .oficina_repository import OficinaRepository
from .conexion_repository import ConexionRepository
from .clip_repository import ClipRepository
from .usuario_repository import UsuarioRepository
from .evento_repository import EventoRepository
from .notificacion_repository import NotificacionRepository
from .reporte_repository import ReporteRepository
from .inference_request_repository import InferenceRequestRepository

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



