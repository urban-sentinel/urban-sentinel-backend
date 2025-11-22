"""
Domain entity: Connection/Camera (no infrastructure dependencies).
"""
from dataclasses import dataclass
from typing import Optional
from datetime import datetime

from ..enums import ModoIngesta


@dataclass
class Conexion:
    """
    Domain entity representing an RTSP camera.
    """
    id_oficina: int
    nombre_camara: str
    rtsp_url: str
    modo_ingesta: ModoIngesta
    habilitada: bool
    retention_minutes: int
    ubicacion: Optional[str] = None
    estado: Optional[str] = None
    ultimo_ping: Optional[datetime] = None
    fps_sample: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    id: Optional[int] = None
    
    def __post_init__(self):
        """Domain validations"""
        if not self.nombre_camara or not self.nombre_camara.strip():
            raise ValueError("nombre_camara cannot be empty")
        
        if len(self.nombre_camara) > 120:
            raise ValueError("nombre_camara cannot exceed 120 characters")
        
        if not self.rtsp_url or not self.rtsp_url.strip():
            raise ValueError("rtsp_url cannot be empty")
        
        if not self.rtsp_url.startswith(('rtsp://', 'rtmp://')):
            raise ValueError("rtsp_url must start with rtsp:// or rtmp://")
        
        if self.retention_minutes < 0:
            raise ValueError("retention_minutes must be >= 0")
        
        if self.fps_sample is not None and self.fps_sample <= 0:
            raise ValueError("fps_sample must be > 0 if specified")
    
    def is_active(self) -> bool:
        """Checks if the camera is active"""
        return self.habilitada and self.estado == "activa"