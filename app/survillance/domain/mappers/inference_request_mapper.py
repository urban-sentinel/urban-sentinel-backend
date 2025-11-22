"""
Mapper para InferenceRequest: conversión entre entidad de dominio y modelo ORM.
"""
from typing import Optional

from app.survillance.models.inference_request_model import InferenceRequest as InferenceRequestORM
from app.survillance.domain.entities.inference_request import InferenceRequest
from ._helpers import _as_dt


def inference_request_to_domain(orm: InferenceRequestORM) -> InferenceRequest:
    """Convierte modelo ORM a entidad de dominio"""
    return InferenceRequest(
        request_id=orm.request_id,
        received_at=orm.received_at,  # ORM ya devuelve datetime con tz
        id=orm.id
    )


def inference_request_to_orm(
    entity: InferenceRequest,
    existing: Optional[InferenceRequestORM] = None
) -> InferenceRequestORM:
    """Convierte entidad de dominio a modelo ORM"""
    orm = existing or InferenceRequestORM()
    
    # NO setear id si entity.id es None (autoincrement)
    if entity.id is not None:
        orm.id = entity.id
    
    orm.request_id = entity.request_id
    # received_at es requerido en dominio, pero si viene None el ORM usará default
    if entity.received_at is not None:
        orm.received_at = _as_dt(entity.received_at)
    
    return orm

