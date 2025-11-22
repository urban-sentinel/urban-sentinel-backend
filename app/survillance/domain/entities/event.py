"""
Domain entity: Event (no infrastructure dependencies).
"""
from dataclasses import dataclass
from typing import Optional
from datetime import datetime

from ..value_objects.timestamps import DurationSeconds, MilliSeconds
from ..value_objects.media_paths import SubclipPath
from ..enums import TipoEvento


@dataclass
class Evento:
    """
    Domain entity representing a detected security event.
    """
    id_conexion: int
    tipo_evento: TipoEvento
    t_inicio_ms: MilliSeconds
    t_fin_ms: MilliSeconds
    timestamp_evento: datetime
    procesado: bool
    id_clip: Optional[int] = None
    id_usuario: Optional[int] = None
    confianza: Optional[float] = None
    subclip_path: Optional[SubclipPath] = None
    subclip_duracion_sec: Optional[DurationSeconds] = None
    id: Optional[int] = None
    
    def __post_init__(self):
        """Domain validations"""
        if self.confianza is not None:
            if not (0.0 <= self.confianza <= 1.0):
                raise ValueError(f"confianza must be between 0.0 and 1.0, received: {self.confianza}")
        
        if int(self.t_inicio_ms) > int(self.t_fin_ms):
            raise ValueError(f"t_inicio_ms ({self.t_inicio_ms}) cannot be greater than t_fin_ms ({self.t_fin_ms})")
    
    def duracion_ms(self) -> MilliSeconds:
        """Calculates the event duration in milliseconds"""
        return MilliSeconds(int(self.t_fin_ms) - int(self.t_inicio_ms))
    
    def tiene_subclip(self) -> bool:
        """Checks if the event has a generated subclip"""
        return self.subclip_path is not None
    
    def is_high_confidence(self, threshold: float = 0.8) -> bool:
        """Checks if the event has high confidence"""
        if self.confianza is None:
            return False
        return self.confianza >= threshold