"""
Domain entity: Clip (no infrastructure dependencies).
"""
from dataclasses import dataclass
from typing import Optional
from datetime import datetime, timedelta

from ..value_objects.timestamps import DurationSeconds
from ..value_objects.media_paths import StoragePath


@dataclass
class Clip:
    """
    Domain entity representing a segmented video clip.
    """
    id_conexion: int
    storage_path: StoragePath
    start_time_utc: datetime
    duration_sec: DurationSeconds
    fecha_guardado: Optional[datetime] = None
    id: Optional[int] = None
    
    def __post_init__(self):
        """Domain validations"""
        # StoragePath and DurationSeconds already validate in their constructors
        pass
    
    def end_time_utc(self) -> datetime:
        """Calculates the end time of the clip"""
        end = self.start_time_utc + timedelta(seconds=int(self.duration_sec))
        return end
    
    def contains_timestamp(self, timestamp: datetime) -> bool:
        """Checks if a timestamp is within the clip"""
        return (self.start_time_utc <= timestamp < self.end_time_utc())