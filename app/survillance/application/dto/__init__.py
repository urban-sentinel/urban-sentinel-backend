"""
DTOs: exportaciones centralizadas.
"""
# Auth DTOs
from .auth_dto import (
    RegisterRequest,
    LoginRequest,
    TokenResponse,
    RefreshRequest,
    UserResponse,
    ChangePasswordRequest,
    ForgotPasswordRequest,
    ValidateTokenRequest,
    DeleteUserRequest
)

# Oficina DTOs
from .oficina_dto import (
    OficinaCreate,
    OficinaUpdate,
    OficinaResponse,
)

# Conexion DTOs
from .conexion_dto import (
    ConexionCreate,
    ConexionUpdate,
    ConexionResponse,
)

# Clip DTOs
from .clip_dto import ClipResponse

# Evento DTOs
from .evento_dto import EventoResponse

# Notificacion DTOs
from .notificacion_dto import (
    NotificacionCreate,
    NotificacionUpdate,
    NotificacionResponse,
)

# Reporte DTOs
from .reporte_dto import (
    ReporteCreate,
    ReporteResponse,
)

# Inference DTOs
from .inference_dto import (
    EventoInferenciaBase,
    EventoInferenciaA,
    EventoInferenciaB,
    InferenceWebhookRequestA,
    InferenceWebhookRequestB,
    InferenceWebhookResponse,
)

__all__ = [
    # Auth
    "UserResponse",
    "RegisterRequest",
    "LoginRequest",
    "TokenResponse",
    "RefreshRequest",
    "ChangePasswordRequest",
    "ForgotPasswordRequest",
    "ValidateTokenRequest",
    "DeleteUserRequest",
    # Oficina
    "OficinaCreate",
    "OficinaUpdate",
    "OficinaResponse",
    # Conexion
    "ConexionCreate",
    "ConexionUpdate",
    "ConexionResponse",
    # Clip
    "ClipResponse",
    # Evento
    "EventoResponse",
    # Notificacion
    "NotificacionCreate",
    "NotificacionUpdate",
    "NotificacionResponse",
    # Reporte
    "ReporteCreate",
    "ReporteResponse",
    # Inference
    "EventoInferenciaBase",
    "EventoInferenciaA",
    "EventoInferenciaB",
    "InferenceWebhookRequestA",
    "InferenceWebhookRequestB",
    "InferenceWebhookResponse",
]



