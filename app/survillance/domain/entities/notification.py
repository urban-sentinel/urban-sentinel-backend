"""
Domain entity: Notification (no infrastructure dependencies).
"""
from dataclasses import dataclass
from typing import Optional
from datetime import datetime

from ..enums import EstadoNotificacion


@dataclass
class Notificacion:
    """
    Domain entity representing an event notification.
    """
    mensaje: str
    canal: str
    destinatario: str
    estado: EstadoNotificacion
    fecha_envio: Optional[datetime] = None
    id: Optional[int] = None
    
    def __post_init__(self):
        """Domain validations"""
        if not self.canal or not self.canal.strip():
            raise ValueError("canal cannot be empty")
        
        if not self.destinatario or not self.destinatario.strip():
            raise ValueError("destinatario cannot be empty")
        
        # If sent, must have send date
        if self.estado == EstadoNotificacion.ENVIADA and self.fecha_envio is None:
            raise ValueError("A sent notification must have fecha_envio")
    
    def is_sent(self) -> bool:
        """Checks if the notification was sent"""
        return self.estado == EstadoNotificacion.ENVIADA
    
    def has_failed(self) -> bool:
        """Checks if the notification failed"""
        return self.estado == EstadoNotificacion.FALLIDA