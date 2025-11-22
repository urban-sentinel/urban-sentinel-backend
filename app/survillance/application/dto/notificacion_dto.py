"""
DTOs para Notificacion.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class NotificacionCreate(BaseModel):
    """Request para crear notificación"""
    mensaje: Optional[str] = Field(None, max_length=500)
    canal: Optional[str] = Field(None, max_length=50)
    destinatario: Optional[str] = Field(None, max_length=150)


class NotificacionUpdate(BaseModel):
    """Request para actualizar notificación"""
    estado: Optional[str] = Field(None, max_length=50)
    fecha_envio: Optional[datetime] = None


class NotificacionResponse(BaseModel):
    """Response de notificación"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    mensaje: Optional[str] = Field(None, max_length=500)
    canal: Optional[str]
    destinatario: Optional[str]
    estado: str
    fecha_envio: Optional[datetime]



