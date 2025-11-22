import asyncio
from typing import Dict
from app.shared.db import AsyncSessionLocal
from app.survillance.infrastructure.repositories import ConexionRepository
from app.survillance.ingestion.camera_worker import CameraWorker

class CameraSupervisor:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self.workers: Dict[int, CameraWorker] = {}
        self._lock = asyncio.Lock()
        self._initialized = True

    async def start_all(self):
        async with AsyncSessionLocal() as session:
            repo = ConexionRepository(session)
            # ⬇️ coincide con tu repo: list_enabled()
            conexiones = await repo.list_enabled()

        # arranca en paralelo, pero filtra primero
        tasks = [
            self.start_camera(c.id_conexion)
            for c in conexiones
            if getattr(c, "modo_ingesta", "SEGMENT") == "SEGMENT"
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for r in results:
            if isinstance(r, Exception):
                # loggea si quieres
                pass

    async def start_camera(self, id_conexion: int):
        async with self._lock:
            if id_conexion in self.workers and self.workers[id_conexion].is_running():
                print(f"Cámara {id_conexion} ya está en ejecución")
                return

            # lee configuración
            async with AsyncSessionLocal() as session:
                repo = ConexionRepository(session)
                # ⬇️ coincide con tu repo: get()
                conexion = await repo.get(id_conexion)

            if not conexion:
                raise ValueError(f"Cámara {id_conexion} no encontrada")
            if not getattr(conexion, "habilitada", True):
                raise ValueError(f"Cámara {id_conexion} no está habilitada")

            # crea/arranca worker
            worker = CameraWorker(conexion)
            try:
                await worker.start()
            except Exception:
                # no dejes estado inconsistente
                raise
            else:
                self.workers[id_conexion] = worker

        # fuera del lock, actualiza estado en BD
        async with AsyncSessionLocal() as session:
            repo = ConexionRepository(session)
            conexion = await repo.get(id_conexion)
            if conexion:
                conexion.estado = "activa"
                await repo.update(conexion)
                await session.commit()

    async def stop_camera(self, id_conexion: int):
        async with self._lock:
            worker = self.workers.get(id_conexion)
            if not worker:
                print(f"Cámara {id_conexion} no está en ejecución")
                return
            await worker.stop()
            self.workers.pop(id_conexion, None)

        async with AsyncSessionLocal() as session:
            repo = ConexionRepository(session)
            conexion = await repo.get(id_conexion)
            if conexion:
                conexion.estado = "inactiva"
                await repo.update(conexion)
                await session.commit()

    async def stop_all(self):
        # copia para no mutar mientras iteras
        ids = list(self.workers.keys())
        await asyncio.gather(*(self.stop_camera(cid) for cid in ids))

    def get_status(self) -> Dict[int, dict]:
        return {
            cid: {
                "running": wk.is_running(),
                "conexion_id": wk.conexion.id,
                "nombre_camara": getattr(wk.conexion, "nombre_camara", ""),
            }
            for cid, wk in self.workers.items()
        }

    def is_camera_running(self, id_conexion: int) -> bool:
        wk = self.workers.get(id_conexion)
        return bool(wk and wk.is_running())


camera_supervisor = CameraSupervisor()
