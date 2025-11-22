"""
SQLAlchemy 2.0 ORM model for User.
"""
from datetime import datetime
from typing import Optional

from sqlalchemy import Integer, String, TIMESTAMP
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.shared.db import Base
from app.shared.time import now_utc


class Usuario(Base):
    """System user with JWT authentication"""
    __tablename__ = "usuarios"
    
    id_usuario: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    apellido: Mapped[Optional[str]] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(150), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    rol: Mapped[Optional[str]] = mapped_column(String(60))
    phone: Mapped[Optional[str]] = mapped_column(String(20))
    fecha_creacion: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=now_utc
    )
    ultimo_login: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP(timezone=True))
    
    # Relationships
    eventos: Mapped[list["Evento"]] = relationship(
        "Evento",
        back_populates="usuario"
    )
    reportes: Mapped[list["Reporte"]] = relationship(
        "Reporte",
        back_populates="usuario"
    )

