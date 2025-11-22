"""
SQLAlchemy 2.0 ORM model for Notification.
"""
from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, Integer, String, TIMESTAMP
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.shared.time import now_utc

from app.shared.db import Base


class Notificacion(Base):
    """Notification sent for an event"""
    __tablename__ = "notificaciones"
    
    id_notificacion: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    mensaje: Mapped[Optional[str]] = mapped_column(String(500))
    canal: Mapped[Optional[str]] = mapped_column(String(50))
    destinatario: Mapped[Optional[str]] = mapped_column(String(150))
    estado: Mapped[str] = mapped_column(String(50), default="pendiente")
    fecha_envio: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP(timezone=True), default=now_utc)