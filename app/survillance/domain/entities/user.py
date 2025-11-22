"""
Domain entity: User (no infrastructure dependencies).
"""
from dataclasses import dataclass
from typing import Optional
import re
from datetime import datetime


@dataclass
class Usuario:
    """
    Domain entity representing a system user.
    """
    nombre: str
    email: str
    password_hash: str
    apellido: Optional[str] = None
    rol: Optional[str] = None
    phone: Optional[str] = None
    fecha_creacion: Optional[datetime] = None
    ultimo_login: Optional[datetime] = None
    id: Optional[int] = None

    def __post_init__(self):
        """Domain validations"""
        if not self.nombre or not self.nombre.strip():
            raise ValueError("nombre cannot be empty")
        
        if len(self.nombre) > 100:
            raise ValueError("nombre cannot exceed 100 characters")
        
        if not self.email or not self.email.strip():
            raise ValueError("email cannot be empty")
        
        # Basic email validation
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, self.email):
            raise ValueError(f"invalid email: {self.email}")
        
        if not self.password_hash or not self.password_hash.strip():
            raise ValueError("password_hash cannot be empty")
    
    def full_name(self) -> str:
        """Returns the full name"""
        if self.apellido:
            return f"{self.nombre} {self.apellido}"
        return self.nombre