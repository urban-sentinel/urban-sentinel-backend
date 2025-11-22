"""
Domain entity: InferenceRequest (webhook idempotency control).
"""
from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class InferenceRequest:
    """
    Domain entity for inference webhook idempotency control.
    Ensures that a request_id is only processed once.
    """
    request_id: str
    received_at: datetime
    id: Optional[int] = None
    
    def __post_init__(self):
        """Domain validations"""
        if not self.request_id or not self.request_id.strip():
            raise ValueError("request_id cannot be empty")
        
        if len(self.request_id) > 64:
            raise ValueError("request_id cannot exceed 64 characters")
    
    def is_duplicate(self) -> bool:
        """
        Checks if this request was already processed.
        In practice, if the entity exists in DB, it's a duplicate.
        """
        return True  # If the instance exists, it was already processed