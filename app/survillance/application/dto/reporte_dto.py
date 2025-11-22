"""
DTOs para Reporte.
"""
from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class ReporteCreate(BaseModel):
    """Request para crear reporte"""
    id_clip: Optional[int] = None
    titulo: Optional[str] = Field(None, max_length=200)
    descripcion: Optional[str] = None
    rango_fecha_inicio: Optional[datetime] = None
    rango_fecha_fin: Optional[datetime] = None
    filtro_confianza: Optional[Decimal] = None
    tipo_evento: Optional[str] = Field(None, max_length=50)


class ReporteResponse(BaseModel):
    """Response de reporte"""
    model_config = ConfigDict(from_attributes=True)
    
    id_reporte: int
    id_usuario: int
    id_clip: Optional[int]
    titulo: Optional[str]
    descripcion: Optional[str]
    rango_fecha_inicio: Optional[datetime]
    rango_fecha_fin: Optional[datetime]
    filtro_confianza: Optional[Decimal]
    tipo_evento: Optional[str]
    fecha_generacion: datetime



