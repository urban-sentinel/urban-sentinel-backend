"""
Modelo ORM de SQLAlchemy 2.0 para InferenceRequest.
"""
from datetime import datetime

from sqlalchemy import Integer, String, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.db import Base
from app.shared.time import now_utc


class InferenceRequest(Base):
    """Control de idempotencia para webhooks de inferencia"""
    __tablename__ = "inference_requests"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    request_id: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    received_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=now_utc,
        nullable=False
    )

