"""
Value Objects para timestamps y duraciones con validación.
"""
from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass(frozen=True)
class UtcDatetime:
    """Datetime que garantiza timezone UTC"""
    value: datetime
    
    def __post_init__(self):
        if self.value.tzinfo is None:
            # Si no tiene timezone, asumimos UTC
            object.__setattr__(self, 'value', self.value.replace(tzinfo=timezone.utc))
        elif self.value.tzinfo != timezone.utc:
            # Convertir a UTC
            object.__setattr__(self, 'value', self.value.astimezone(timezone.utc))
    
    def to_datetime(self) -> datetime:
        """Retorna el datetime subyacente"""
        return self.value
    
    def __str__(self) -> str:
        return self.value.isoformat()


@dataclass(frozen=True)
class DurationSeconds:
    """Duración en segundos (>=0)"""
    value: int
    
    def __post_init__(self):
        if self.value < 0:
            raise ValueError(f"DurationSeconds debe ser >= 0, recibido: {self.value}")
    
    def __int__(self) -> int:
        return self.value
    
    def __str__(self) -> str:
        return f"{self.value}s"


@dataclass(frozen=True)
class MilliSeconds:
    """Milisegundos (>=0) para offsets en clips"""
    value: int
    
    def __post_init__(self):
        if self.value < 0:
            raise ValueError(f"MilliSeconds debe ser >= 0, recibido: {self.value}")
    
    def __int__(self) -> int:
        return self.value
    
    def __str__(self) -> str:
        return f"{self.value}ms"
    
    def to_seconds(self) -> float:
        """Convierte a segundos"""
        return self.value / 1000.0