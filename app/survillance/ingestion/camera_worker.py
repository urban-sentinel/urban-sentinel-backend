"""
Worker de cámara: gestiona FFmpeg para segmentar RTSP y registra clips en BD.
"""
import asyncio
import os
from pathlib import Path
from datetime import datetime
from typing import Optional

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from app.config.settings import settings
from app.shared.db import AsyncSessionLocal
from app.shared.time import filename_to_utc, now_utc
from app.survillance.domain.entities import Clip, Conexion
from app.survillance.infrastructure.repositories import ClipRepository


class VideoFileHandler(FileSystemEventHandler):
    """Handler para detectar nuevos clips cerrados"""
    
    def __init__(self, id_conexion: int):
        self.id_conexion = id_conexion
        self.pending_clips = asyncio.Queue()
    
    def on_created(self, event):
        """Se llama cuando se crea un archivo"""
        if event.is_directory:
            return
        
        if event.src_path.endswith('.mp4'):
            # Esperar a que el archivo se cierre (simplificado)
            asyncio.create_task(self._process_new_clip(event.src_path))
    
    async def _process_new_clip(self, filepath: str):
        """Procesa un nuevo clip cuando está cerrado"""
        # Esperar que FFmpeg cierre el archivo
        await asyncio.sleep(2)
        
        # Verificar que existe y tiene tamaño
        if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
            await self.pending_clips.put(filepath)


class CameraWorker:
    """Worker que gestiona la ingesta de una cámara específica"""
    
    def __init__(self, conexion: Conexion):
        self.conexion = conexion
        self.process: Optional[asyncio.subprocess.Process] = None
        self.running = False
        self.observer: Optional[any] = None
        self.handler: Optional[VideoFileHandler] = None
    
    async def start(self):
        """Inicia la ingesta de la cámara"""
        if self.running:
            return
        
        self.running = True
        
        # Crear directorio de salida
        base_path = os.path.join(
            settings.STORAGE_BASE_PATH,
            f"cam_{self.conexion.id}",
            "clips"
        )
        Path(base_path).mkdir(parents=True, exist_ok=True)
        
        # Patrón de salida con estructura de fecha
        output_pattern = os.path.join(
            base_path,
            "%Y", "%m", "%d",
            f"clip_%Y%m%d_%H%M%S.mp4"
        )
        
        # Comando FFmpeg
        cmd = [
            settings.FFMPEG_PATH,
            "-rtsp_transport", "tcp",
            "-i", self.conexion.rtsp_url,
            "-c", "copy",
            "-f", "segment",
            "-segment_time", str(settings.SEGMENT_SECONDS),
            "-reset_timestamps", "1",
            "-strftime", "1",
            output_pattern
        ]
        
        # Iniciar proceso FFmpeg
        try:
            self.process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            print(f"FFmpeg iniciado para cámara {self.conexion.id}")
            
            # Iniciar watchdog para detectar archivos
            self.handler = VideoFileHandler(self.conexion.id)
            self.observer = Observer()
            self.observer.schedule(self.handler, base_path, recursive=True)
            self.observer.start()
            
            # Iniciar tarea de registro de clips
            asyncio.create_task(self._register_clips_loop())
            
            # Monitorear stderr de FFmpeg
            asyncio.create_task(self._monitor_ffmpeg())
            
        except Exception as e:
            print(f"Error iniciando FFmpeg para cámara {self.conexion.id_conexion}: {e}")
            self.running = False
            raise
    
    async def stop(self):
        """Detiene la ingesta de la cámara"""
        if not self.running:
            return
        
        self.running = False
        
        # Detener watchdog
        if self.observer:
            self.observer.stop()
            self.observer.join()
        
        # Terminar proceso FFmpeg
        if self.process:
            self.process.terminate()
            try:
                await asyncio.wait_for(self.process.wait(), timeout=5.0)
            except asyncio.TimeoutError:
                self.process.kill()
                await self.process.wait()
        
        print(f"FFmpeg detenido para cámara {self.conexion.id}")
    
    async def _register_clips_loop(self):
        """Loop que registra clips en la BD"""
        while self.running:
            try:
                # Esperar nuevo clip (con timeout)
                filepath = await asyncio.wait_for(
                    self.handler.pending_clips.get(),
                    timeout=1.0
                )
                
                await self._register_clip(filepath)
                
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                print(f"Error registrando clip: {e}")
    
    async def _register_clip(self, filepath: str):
        """Registra un clip en la BD"""
        try:
            # Extraer timestamp del nombre de archivo
            filename = os.path.basename(filepath)
            start_time = filename_to_utc(filename)
            
            if not start_time:
                print(f"No se pudo extraer timestamp de {filename}")
                return
            
            # Obtener duración (simplificado, asumir segment_seconds)
            duration_sec = settings.SEGMENT_SECONDS
            
            # Crear registro en BD
            async with AsyncSessionLocal() as session:
                clip_repo = ClipRepository(session)
                
                clip = Clip(
                    id_conexion=self.conexion.id,
                    storage_path=filepath,
                    start_time_utc=start_time,
                    duration_sec=duration_sec,
                    fecha_guardado=now_utc()
                )
                
                await clip_repo.create(clip)
                await session.commit()
            
            print(f"Clip registrado: {filename}")
            
        except Exception as e:
            print(f"Error al registrar clip {filepath}: {e}")
    
    async def _monitor_ffmpeg(self):
        """Monitorea stderr de FFmpeg para detectar errores"""
        if not self.process or not self.process.stderr:
            return
        
        while self.running:
            try:
                line = await self.process.stderr.readline()
                if not line:
                    break
                
                # Log de errores (simplificado)
                line_str = line.decode().strip()
                if "error" in line_str.lower():
                    print(f"FFmpeg error (cámara {self.conexion.id}): {line_str}")
                    
            except Exception:
                break
    
    def is_running(self) -> bool:
        """Verifica si el worker está corriendo"""
        return self.running and self.process is not None