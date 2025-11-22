"""
Domain entity: Report (no infrastructure dependencies).
"""
from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Reporte:
    """
    Domain entity representing a user-generated report.
    """
    id_usuario: int
    titulo: str
    descripcion: Optional[str] = None
    id_clip: Optional[int] = None
    rango_fecha_inicio: Optional[datetime] = None
    rango_fecha_fin: Optional[datetime] = None
    filtro_confianza: Optional[float] = None
    tipo_evento: Optional[str] = None
    fecha_generacion: Optional[datetime] = None
    id: Optional[int] = None
    
    def __post_init__(self):
        """Domain validations"""
        if not self.titulo or not self.titulo.strip():
            raise ValueError("titulo cannot be empty")
        
        if len(self.titulo) > 200:
            raise ValueError("titulo cannot exceed 200 characters")
        
        if self.filtro_confianza is not None:
            if not (0.0 <= self.filtro_confianza <= 1.0):
                raise ValueError(f"filtro_confianza must be between 0.0 and 1.0, received: {self.filtro_confianza}")
        
        # Validate that fecha_inicio < fecha_fin if both exist
        if (self.rango_fecha_inicio and self.rango_fecha_fin and 
            self.rango_fecha_inicio >= self.rango_fecha_fin):
            raise ValueError("rango_fecha_inicio must be before rango_fecha_fin")
    
    def has_date_range(self) -> bool:
        """Checks if the report has a date range"""
        return self.rango_fecha_inicio is not None and self.rango_fecha_fin is not None