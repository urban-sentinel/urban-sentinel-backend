"""
DTOs para Oficina.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class OficinaCreate(BaseModel):
    """Request para crear oficina"""
    nombre_oficina: str = Field(..., max_length=150)
    direccion: Optional[str] = Field(None, max_length=255)
    ciudad: Optional[str] = Field(None, max_length=100)
    responsable: Optional[str] = Field(None, max_length=100)
    telefono_contacto: Optional[str] = Field(None, max_length=50)


class OficinaUpdate(BaseModel):
    """Request para actualizar oficina"""
    nombre_oficina: Optional[str] = Field(None, max_length=150)
    direccion: Optional[str] = Field(None, max_length=255)
    ciudad: Optional[str] = Field(None, max_length=100)
    responsable: Optional[str] = Field(None, max_length=100)
    telefono_contacto: Optional[str] = Field(None, max_length=50)


class OficinaResponse(BaseModel):
    """Response de oficina"""
    model_config = ConfigDict(from_attributes=True)
    
    id_oficina: int
    nombre_oficina: str
    direccion: Optional[str]
    ciudad: Optional[str]
    responsable: Optional[str]
    telefono_contacto: Optional[str]
    fecha_registro: datetime



