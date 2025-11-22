"""
Servicio de retención: elimina clips viejos según retention_minutes de cada cámara.
"""
import os
from datetime import datetime, timedelta
from typing import Dict, List

from app.shared.time import now_utc
from app.survillance.domain.repositories_interfaces import IConexionRepository, IClipRepository
from app.survillance.domain.entities import Conexion


class RetentionService:
    """Servicio para aplicar políticas de retención de clips"""
    
    def __init__(
        self,
        conexion_repo: IConexionRepository,
        clip_repo: IClipRepository
    ):
        self.conexion_repo = conexion_repo
        self.clip_repo = clip_repo
    
    async def apply_retention(self) -> Dict[str, int]:
        """
        Aplica retención a todas las cámaras habilitadas.
        Elimina clips más viejos que retention_minutes y sus archivos del disco.
        No elimina archivos en carpeta events/ (subclips de eventos).
        
        Returns:
            Dict con stats: {deleted_clips, deleted_files, errors}
        """
        conexiones = await self.conexion_repo.get_enabled()
        
        stats = {
            "deleted_clips": 0,
            "deleted_files": 0,
            "errors": 0
        }
        
        for conexion in conexiones:
            try:
                deleted = await self._apply_retention_for_camera(conexion)
                stats["deleted_clips"] += deleted["clips"]
                stats["deleted_files"] += deleted["files"]
            except Exception as e:
                print(f"Error aplicando retención en cámara {conexion.id}: {e}")
                stats["errors"] += 1
        
        return stats
    
    async def _apply_retention_for_camera(self, conexion: Conexion) -> Dict[str, int]:
        """
        Aplica retención para una cámara específica.
        
        Returns:
            Dict con clips y files eliminados
        """
        cutoff_time = now_utc() - timedelta(minutes=conexion.retention_minutes)
        
        # Obtener clips viejos
        old_clips = await self.clip_repo.get_old_clips(
            conexion.id,
            cutoff_time
        )
        
        deleted_clips = 0
        deleted_files = 0
        
        for clip in old_clips:
            # Verificar que no sea un subclip de evento (en carpeta events/)
            if "/events/" in clip.storage_path or "\\events\\" in clip.storage_path:
                continue
            
            # Eliminar archivo del disco
            if os.path.exists(clip.storage_path):
                try:
                    os.remove(clip.storage_path)
                    deleted_files += 1
                except Exception as e:
                    print(f"Error eliminando archivo {clip.storage_path}: {e}")
            
            # Eliminar registro de BD
            if clip.id is not None:
                await self.clip_repo.delete(clip.id)
                deleted_clips += 1
        
        return {
            "clips": deleted_clips,
            "files": deleted_files
        }
    
    async def get_retention_status(self) -> List[Dict]:
        """
        Obtiene el status de retención de todas las cámaras.
        
        Returns:
            Lista de dicts con info de cada cámara
        """
        conexiones = await self.conexion_repo.get_enabled()
        status_list = []
        
        for conexion in conexiones:
            cutoff_time = now_utc() - timedelta(minutes=conexion.retention_minutes)
            old_clips = await self.clip_repo.get_old_clips(
                conexion.id,
                cutoff_time
            )
            
            status_list.append({
                "id_conexion": conexion.id,
                "nombre_camara": conexion.nombre_camara,
                "retention_minutes": conexion.retention_minutes,
                "clips_to_delete": len(old_clips)
            })
        
        return status_list