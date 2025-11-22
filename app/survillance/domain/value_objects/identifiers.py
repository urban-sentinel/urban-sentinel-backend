"""
Value Objects para identificadores con validación.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class IdOficina:
    """Identificador único de oficina"""
    value: int
    
    def __post_init__(self):
        if self.value <= 0:
            raise ValueError(f"IdOficina debe ser > 0, recibido: {self.value}")
    
    def __int__(self) -> int:
        return self.value
    
    def __str__(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class IdConexion:
    """Identificador único de conexión/cámara"""
    value: int
    
    def __post_init__(self):
        if self.value <= 0:
            raise ValueError(f"IdConexion debe ser > 0, recibido: {self.value}")
    
    def __int__(self) -> int:
        return self.value
    
    def __str__(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class IdClip:
    """Identificador único de clip"""
    value: int
    
    def __post_init__(self):
        if self.value <= 0:
            raise ValueError(f"IdClip debe ser > 0, recibido: {self.value}")
    
    def __int__(self) -> int:
        return self.value
    
    def __str__(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class IdEvento:
    """Identificador único de evento"""
    value: int
    
    def __post_init__(self):
        if self.value <= 0:
            raise ValueError(f"IdEvento debe ser > 0, recibido: {self.value}")
    
    def __int__(self) -> int:
        return self.value
    
    def __str__(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class IdUsuario:
    """Identificador único de usuario"""
    value: int
    
    def __post_init__(self):
        if self.value <= 0:
            raise ValueError(f"IdUsuario debe ser > 0, recibido: {self.value}")
    
    def __int__(self) -> int:
        return self.value
    
    def __str__(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class IdReporte:
    """Identificador único de reporte"""
    value: int
    
    def __post_init__(self):
        if self.value <= 0:
            raise ValueError(f"IdReporte debe ser > 0, recibido: {self.value}")
    
    def __int__(self) -> int:
        return self.value
    
    def __str__(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class IdNotificacion:
    """Identificador único de notificación"""
    value: int
    
    def __post_init__(self):
        if self.value <= 0:
            raise ValueError(f"IdNotificacion debe ser > 0, recibido: {self.value}")
    
    def __int__(self) -> int:
        return self.value
    
    def __str__(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class IdInferenceRequest:
    """Identificador único de inference request"""
    value: int
    
    def __post_init__(self):
        if self.value <= 0:
            raise ValueError(f"IdInferenceRequest debe ser > 0, recibido: {self.value}")
    
    def __int__(self) -> int:
        return self.value
    
    def __str__(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class IdEventSnapshot:
    """Identificador único de event snapshot"""
    value: int
    
    def __post_init__(self):
        if self.value <= 0:
            raise ValueError(f"IdEventSnapshot debe ser > 0, recibido: {self.value}")
    
    def __int__(self) -> int:
        return self.value
    
    def __str__(self) -> str:
        return str(self.value)