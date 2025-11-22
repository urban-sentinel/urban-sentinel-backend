"""
DTOs para Clip.
"""
from datetime import datetime
from typing import Any
from pydantic import BaseModel, ConfigDict, model_validator


class ClipResponse(BaseModel):
    """Response de clip"""
    model_config = ConfigDict(from_attributes=True)

    id_clip: int
    id_conexion: int
    storage_path: str
    start_time_utc: datetime
    duration_sec: int
    fecha_guardado: datetime

    @model_validator(mode="before")
    @classmethod
    def _from_domain(cls, obj: Any):
        # Si ya es dict con primitivos, lo dejamos
        if isinstance(obj, dict):
            if "id_clip" not in obj and "id" in obj:
                obj = {**obj, "id_clip": obj.get("id")}
            return obj

        # Helper para extraer .value de VOs/Enums
        def val(x):
            if x is None:
                return None
            return getattr(x, "value", x)

        return {
            "id_clip": getattr(obj, "id", getattr(obj, "id_clip", None)),
            "id_conexion": getattr(obj, "id_conexion", None),
            "storage_path": val(getattr(obj, "storage_path", None)),
            "start_time_utc": getattr(obj, "start_time_utc", None),
            "duration_sec": int(val(getattr(obj, "duration_sec", None)) or 0),
            "fecha_guardado": getattr(obj, "fecha_guardado", None),
        }



