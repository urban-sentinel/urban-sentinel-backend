"""
DTOs para Conexion.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class ConexionCreate(BaseModel):
    """Request para crear conexión"""
    id_oficina: int
    nombre_camara: str = Field(..., max_length=120)
    ubicacion: Optional[str] = Field(None, max_length=255)
    rtsp_url: str
    modo_ingesta: str = Field(default="SEGMENT", max_length=20)
    fps_sample: Optional[int] = None
    habilitada: bool = True
    retention_minutes: int = 60


class ConexionUpdate(BaseModel):
    """Request para actualizar conexión"""
    nombre_camara: Optional[str] = Field(None, max_length=120)
    ubicacion: Optional[str] = Field(None, max_length=255)
    rtsp_url: Optional[str] = None
    estado: Optional[str] = Field(None, max_length=50)
    modo_ingesta: Optional[str] = Field(None, max_length=20)
    fps_sample: Optional[int] = None
    habilitada: Optional[bool] = None
    retention_minutes: Optional[int] = None


class ConexionResponse(BaseModel):
    """Response de conexión"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    id_oficina: int
    nombre_camara: str
    ubicacion: Optional[str]
    rtsp_url: str
    estado: Optional[str]
    ultimo_ping: Optional[datetime]
    modo_ingesta: str
    fps_sample: Optional[int]
    habilitada: bool
    retention_minutes: int
    created_at: datetime
    updated_at: Optional[datetime]



