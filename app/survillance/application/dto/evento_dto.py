"""
DTOs para Evento.
"""
from datetime import datetime
from decimal import Decimal
from typing import Optional, Any
from pydantic import BaseModel, ConfigDict, model_validator


class EventoResponse(BaseModel):
    """Response de evento"""
    model_config = ConfigDict(from_attributes=True)

    id_evento: int
    id_conexion: int
    id_clip: Optional[int]
    id_usuario: Optional[int]
    tipo_evento: str
    confianza: Optional[Decimal]
    t_inicio_ms: Optional[int]
    t_fin_ms: Optional[int]
    timestamp_evento: datetime
    procesado: bool
    subclip_path: Optional[str]
    subclip_duracion_sec: Optional[int]

    @model_validator(mode="before")
    @classmethod
    def _from_domain(cls, obj: Any):
        if isinstance(obj, dict):
            # Acepta dicts y mapea id -> id_evento si fuera el caso
            if "id_evento" not in obj and "id" in obj:
                obj = {**obj, "id_evento": obj.get("id")}
            return obj

        def val(x):
            if x is None:
                return None
            return getattr(x, "value", x)

        # Normaliza confianza a Decimal si viene float
        raw_conf = getattr(obj, "confianza", None)
        if raw_conf is not None and not isinstance(raw_conf, Decimal):
            try:
                raw_conf = Decimal(str(val(raw_conf)))
            except Exception:
                raw_conf = None

        return {
            "id_evento": getattr(obj, "id", getattr(obj, "id_evento", None)),
            "id_conexion": getattr(obj, "id_conexion", None),
            "id_clip": getattr(obj, "id_clip", None),
            "id_usuario": getattr(obj, "id_usuario", None),
            "tipo_evento": str(val(getattr(obj, "tipo_evento", None))),
            "confianza": raw_conf,
            "t_inicio_ms": (int(val(getattr(obj, "t_inicio_ms", None))) 
                            if getattr(obj, "t_inicio_ms", None) is not None else None),
            "t_fin_ms": (int(val(getattr(obj, "t_fin_ms", None)))
                        if getattr(obj, "t_fin_ms", None) is not None else None),
            "timestamp_evento": getattr(obj, "timestamp_evento", None),
            "procesado": bool(getattr(obj, "procesado", False)),
            "subclip_path": val(getattr(obj, "subclip_path", None)),
            "subclip_duracion_sec": (int(val(getattr(obj, "subclip_duracion_sec", None)))
                                    if getattr(obj, "subclip_duracion_sec", None) is not None else None),
        }



