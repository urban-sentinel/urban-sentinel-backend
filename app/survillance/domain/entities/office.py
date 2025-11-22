"""
Domain entity: Office (no infrastructure dependencies).
"""
from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Oficina:
    """
    Domain entity representing a physical office.
    """
    nombre_oficina: str
    direccion: Optional[str] = None
    ciudad: Optional[str] = None
    responsable: Optional[str] = None
    telefono_contacto: Optional[str] = None
    fecha_registro: Optional[datetime] = None
    id: Optional[int] = None
    
    def __post_init__(self):
        """Domain validations"""
        if not self.nombre_oficina or not self.nombre_oficina.strip():
            raise ValueError("nombre_oficina cannot be empty")
        
        if len(self.nombre_oficina) > 150:
            raise ValueError("nombre_oficina cannot exceed 150 characters")