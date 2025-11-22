"""
Job periódico para aplicar retención de clips.
"""
import asyncio
from typing import Optional

from app.shared.db import AsyncSessionLocal
from app.survillance.infrastructure.repositories import (
    ConexionRepository,
    ClipRepository
)
from app.survillance.application.retention_service import RetentionService


class RetentionJob:
    """Job que ejecuta retención periódicamente"""
    
    def __init__(self, interval_seconds: int = 60):
        self.interval_seconds = interval_seconds
        self.running = False
        self.task: Optional[asyncio.Task] = None
    
    async def start(self):
        """Inicia el job periódico"""
        if self.running:
            return
        
        self.running = True
        self.task = asyncio.create_task(self._run_loop())
        print(f"Retention job iniciado (cada {self.interval_seconds}s)")
    
    async def stop(self):
        """Detiene el job"""
        if not self.running:
            return
        
        self.running = False
        
        if self.task:
            self.task.cancel()
            try:
                await self.task
            except asyncio.CancelledError:
                pass
        
        print("Retention job detenido")
    
    async def _run_loop(self):
        """Loop principal del job"""
        while self.running:
            try:
                await self._execute_retention()
            except Exception as e:
                print(f"Error en retention job: {e}")
            
            # Esperar intervalo
            await asyncio.sleep(self.interval_seconds)
    
    async def _execute_retention(self):
        """Ejecuta la retención"""
        async with AsyncSessionLocal() as session:
            conexion_repo = ConexionRepository(session)
            clip_repo = ClipRepository(session)
            
            retention_service = RetentionService(conexion_repo, clip_repo)
            stats = await retention_service.apply_retention()
            
            await session.commit()
        
        if stats["deleted_clips"] > 0:
            print(f"Retención aplicada: {stats['deleted_clips']} clips, "
                f"{stats['deleted_files']} archivos eliminados")


# Instancia global del job
retention_job = RetentionJob(interval_seconds=60)