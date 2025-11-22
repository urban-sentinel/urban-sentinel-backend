"""
Domain entity: EventSnapshot (event snapshot/frame).
"""
from dataclasses import dataclass
from typing import Optional

from ..value_objects.timestamps import MilliSeconds
from ..value_objects.media_paths import SnapshotPath


@dataclass
class EventSnapshot:
    """
    Domain entity representing an event snapshot (image).
    Captures a specific frame from the video at the moment of the event.
    """
    id_evento: int
    ruta_imagen: SnapshotPath
    timestamp_rel_ms: MilliSeconds
    id: Optional[int] = None
    
    def __post_init__(self):
        """Domain validations"""
        # SnapshotPath and MilliSeconds already validate in their constructors
        pass
    
    def is_at_event_start(self, tolerance_ms: int = 100) -> bool:
        """
        Checks if the snapshot is near the start of the event.
        
        Args:
            tolerance_ms: Tolerance in milliseconds
        
        Returns:
            True if within the start tolerance
        """
        return int(self.timestamp_rel_ms) <= tolerance_ms