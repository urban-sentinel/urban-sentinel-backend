"""
Resuelve rangos de tiempo absolutos a lista de clips con offsets para corte/concatenación.
"""
from datetime import datetime, timedelta
from typing import List, Tuple

from app.survillance.domain.entities import Clip


class ClipResolver:
    """Resuelve rangos de tiempo a clips específicos con offsets"""
    
    @staticmethod
    def resolve_time_range(
        clips: List[Clip],
        start_time_abs: datetime,
        end_time_abs: datetime
    ) -> List[Tuple[str, float, float]]:
        """
        Dado un rango absoluto y una lista de clips ordenados, retorna lista de
        (storage_path, ss, dur) para cortar cada clip.
        
        Args:
            clips: Lista de clips ordenados por start_time_utc
            start_time_abs: Inicio del rango absoluto (UTC)
            end_time_abs: Fin del rango absoluto (UTC)
        
        Returns:
            Lista de tuplas (storage_path, ss, dur) donde:
            - storage_path: ruta del clip
            - ss: segundo de inicio dentro del clip
            - dur: duración a cortar
        """
        result = []
        
        for clip in clips:
            clip_start = clip.start_time_utc
            duration_sec = int(clip.duration_sec)  # Convertir DurationSeconds VO a int
            clip_end = clip_start + timedelta(seconds=duration_sec)
            
            # Si el clip no intersecta el rango, skip
            if clip_end <= start_time_abs or clip_start >= end_time_abs:
                continue
            
            # Calcular offset de inicio dentro del clip
            if start_time_abs <= clip_start:
                # El rango empieza antes del clip, usar desde el inicio
                ss = 0.0
            else:
                # El rango empieza dentro del clip
                delta = (start_time_abs - clip_start).total_seconds()
                ss = max(0.0, delta)
            
            # Calcular duración a cortar
            if end_time_abs >= clip_end:
                # El rango cubre hasta el final del clip o más
                dur = duration_sec - ss
            else:
                # El rango termina dentro del clip
                delta_end = (end_time_abs - clip_start).total_seconds()
                dur = delta_end - ss
            
            # Asegurar que dur sea positiva
            dur = max(0.1, dur)
            
            # Convertir storage_path a string si es StoragePath VO
            storage_path_str = str(clip.storage_path)
            result.append((storage_path_str, ss, dur))
        
        return result
    
    @staticmethod
    def calculate_absolute_timestamp(
        clip: Clip,
        offset_ms: int
    ) -> datetime:
        """
        Calcula el timestamp absoluto dado un clip y offset en milisegundos.
        
        Args:
            clip: Clip de referencia
            offset_ms: Offset en milisegundos desde el inicio del clip
        
        Returns:
            Timestamp absoluto UTC
        """
        return clip.start_time_utc + timedelta(milliseconds=offset_ms)
    
    @staticmethod
    def calculate_relative_offset(
        clip: Clip,
        timestamp_abs: datetime
    ) -> int:
        """
        Calcula el offset en milisegundos relativo al clip dado un timestamp absoluto.
        
        Args:
            clip: Clip de referencia
            timestamp_abs: Timestamp absoluto UTC
        
        Returns:
            Offset en milisegundos desde el inicio del clip
        """
        delta = (timestamp_abs - clip.start_time_utc).total_seconds()
        return int(delta * 1000)