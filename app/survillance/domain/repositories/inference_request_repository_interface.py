"""
Interfaz de repositorio de InferenceRequest usando typing.Protocol.
"""
from typing import Protocol, Optional

from ..entities.inference_request import InferenceRequest
from ..value_objects.identifiers import IdInferenceRequest


class IInferenceRequestRepository(Protocol):
    """Repositorio de inference requests (idempotencia)"""
    
    async def get(self, id: IdInferenceRequest) -> Optional[InferenceRequest]:
        """Obtiene un inference request por ID"""
        ...
    
    async def get_by_request_id(self, request_id: str) -> Optional[InferenceRequest]:
        """Obtiene un inference request por request_id único"""
        ...
    
    async def exists_by_request_id(self, request_id: str) -> bool:
        """Verifica si un request_id ya existe (idempotencia)"""
        ...
    
    async def create(self, inference_request: InferenceRequest) -> InferenceRequest:
        """Crea un nuevo inference request"""
        ...



