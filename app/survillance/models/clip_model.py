"""
SQLAlchemy 2.0 ORM model for Clip.
"""
from datetime import datetime

from sqlalchemy import ForeignKey, Integer, Text, TIMESTAMP
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.shared.db import Base
from app.shared.time import now_utc


class Clip(Base):
    """Buffer of segmented clips on disk"""
    __tablename__ = "clips"
    
    id_clip: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_conexion: Mapped[int] = mapped_column(ForeignKey("conexiones.id_conexion"), nullable=False)
    storage_path: Mapped[str] = mapped_column(Text, nullable=False)
    start_time_utc: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False)
    duration_sec: Mapped[int] = mapped_column(Integer, nullable=False)
    fecha_guardado: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=now_utc
    )
    
    # Relationships
    conexion: Mapped["Conexion"] = relationship("Conexion", back_populates="clips")
    eventos: Mapped[list["Evento"]] = relationship(
        "Evento",
        back_populates="clip"
    )
    reportes: Mapped[list["Reporte"]] = relationship(
        "Reporte",
        back_populates="clip"
    )

