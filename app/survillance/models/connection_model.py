"""
SQLAlchemy 2.0 ORM model for Connection.
"""
from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, ForeignKey, Integer, String, Text, TIMESTAMP
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.shared.db import Base
from app.shared.time import now_utc


class Conexion(Base):
    """Camera with RTSP configuration and ingestion"""
    __tablename__ = "conexiones"
    
    id_conexion: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_oficina: Mapped[int] = mapped_column(ForeignKey("oficinas.id_oficina"), nullable=False)
    nombre_camara: Mapped[str] = mapped_column(String(120), nullable=False)
    ubicacion: Mapped[Optional[str]] = mapped_column(String(255))
    rtsp_url: Mapped[str] = mapped_column(Text, nullable=False)
    estado: Mapped[Optional[str]] = mapped_column(String(50), default="inactiva")
    ultimo_ping: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP(timezone=True))
    modo_ingesta: Mapped[str] = mapped_column(String(20), default="SEGMENT")
    fps_sample: Mapped[Optional[int]] = mapped_column(Integer)
    habilitada: Mapped[bool] = mapped_column(Boolean, default=True)
    retention_minutes: Mapped[int] = mapped_column(Integer, default=60)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=now_utc
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        TIMESTAMP(timezone=True),
        onupdate=now_utc
    )
    
    # Relationships
    oficina: Mapped["Oficina"] = relationship("Oficina", back_populates="conexiones")
    clips: Mapped[list["Clip"]] = relationship(
        "Clip",
        back_populates="conexion",
        cascade="all, delete-orphan"
    )
    eventos: Mapped[list["Evento"]] = relationship(
        "Evento",
        back_populates="conexion",
        cascade="all, delete-orphan"
    )

