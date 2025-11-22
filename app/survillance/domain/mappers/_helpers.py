"""
Funciones helper compartidas para mappers.
"""
from typing import Optional
from datetime import datetime, timezone


def _as_dt(value) -> Optional[datetime]:
    """
    Normaliza un valor a datetime con timezone UTC.
    Acepta datetime, UtcDatetime VO, o None.
    """
    if value is None:
        return None
    if isinstance(value, datetime):
        # Asegurar que tenga timezone UTC
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc)
    # Si es un value object con .value (ej: UtcDatetime)
    if hasattr(value, 'value'):
        dt = value.value
        if isinstance(dt, datetime):
            if dt.tzinfo is None:
                return dt.replace(tzinfo=timezone.utc)
            return dt.astimezone(timezone.utc)
    # Fallback: intentar usar directamente
    return value

