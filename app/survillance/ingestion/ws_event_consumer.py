from __future__ import annotations

import asyncio
import json
import os
import logging
from dataclasses import dataclass
from typing import Callable, Dict, List, Optional

import websockets

# Services y repos
from app.survillance.application.services.clip_service import ClipService
from app.survillance.application.services.evento_service import EventoService
from app.survillance.infrastructure.repositories import (
    ClipRepository, EventoRepository,
)
from app.survillance.domain.enums import TipoEvento
from datetime import datetime

from app.shared.services.sms_service import TwilioSmsResult, sms_service

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def _build_sms_body(
    *,
    tipo_evento: TipoEvento,
    confianza: float | None,
    camera_id: str | None,
    fecha_evento: datetime,
) -> str:
    if isinstance(confianza, (int, float)):
        confianza_pct = int(max(0.0, min(1.0, float(confianza))) * 100)
        conf_txt = f"{confianza_pct}%"
    else:
        conf_txt = "N/A"

    cam_txt = camera_id or "CAM_01"
    fecha_local = fecha_evento.astimezone()

    return (
        f"[Alerta] {tipo_evento.name.title()} en cámara {cam_txt} | "
        f"Hora: {fecha_local.strftime('%Y-%m-%d %H:%M:%S')} | "
        f"Confianza: {conf_txt}"
    )

# ---------- Configuración ----------
@dataclass
class WsIngestSettings:
    model_ws_base: str = os.getenv("MODEL_WS_BASE", "ws://127.0.0.1:8010")
    cameras: List[str] = None
    conexion_by_camera: Dict[str, int] = None
    reconnect_initial_ms: int = 500
    reconnect_max_ms: int = 5000

    @classmethod
    def from_env(cls) -> "WsIngestSettings":
        cams = os.getenv("MODEL_CAMERAS", "cam_01").split(",")
        mapping: Dict[str, int] = {}
        for cid in cams:
            key = f"MODEL_CAMERA_map__{cid.strip()}"
            if os.getenv(key):
                mapping[cid.strip()] = int(os.getenv(key))
        if not mapping:
            mapping = {cid.strip(): 1 for cid in cams}
        return cls(
            model_ws_base=os.getenv("MODEL_WS_BASE", "ws://127.0.0.1:8010"),
            cameras=[c.strip() for c in cams if c.strip()],
            conexion_by_camera=mapping,
            reconnect_initial_ms=int(os.getenv("WS_RECONNECT_INITIAL_MS", "500")),
            reconnect_max_ms=int(os.getenv("WS_RECONNECT_MAX_MS", "5000")),
        )

# --- Helper para leer el JSON ---
def _read_json_file_sync(file_path: str) -> Optional[dict]:
    """Lee un archivo JSON de forma síncrona."""
    try:
        if not os.path.exists(file_path):
            logger.error("[WS-INGEST] Archivo de log no encontrado: %s", file_path)
            return None
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error("[WS-INGEST] Error leyendo archivo de log %s: %s", file_path, e)
        return None

# --- Helper para extraer top_class y top_prob del contenido ---
def _extract_top_class_and_prob(log_content: dict) -> tuple[str | None, float | None]:
    """Calcula la clase y probabilidad de máxima confianza del evento."""
    logs = log_content.get("logs", [])
    if not logs:
        return None, None

    max_prob = 0.0
    top_class = None

    # Iterar sobre todos los registros de frames
    for log in logs:
        probabilities = log.get("probabilities", {})
        
        # Encontrar la clase con mayor probabilidad en este frame
        if probabilities:
            current_top_class = max(probabilities, key=probabilities.get)
            current_max_prob = probabilities[current_top_class]

            # Si la probabilidad de este frame es la más alta vista hasta ahora
            if current_max_prob > max_prob:
                max_prob = current_max_prob
                top_class = current_top_class.lower() # Aseguramos minúsculas para el mapping

    if top_class and max_prob > 0:
        return top_class, max_prob
    return None, None

def _to_tipo_evento(top_cls: str | None) -> TipoEvento:
    k = (top_cls or "").strip().lower()
    if k == "forcejeo":
        return TipoEvento.FORCEJEO
    if k == "patada":
        return TipoEvento.PATADA
    if k == "golpe":
        return TipoEvento.GOLPE
    # fallback simple y válido para tu BD
    return TipoEvento.FORCEJEO

async def _create_clip_and_event(
    *,
    payload: dict,
    id_conexion: int,
    session_factory: Callable,
):
    """
    Crea Clip y Evento a partir del payload event_complete del modelo.
    """
    # ---------------------------------------------------------------
    # 1. Obtener la máxima confianza, leyendo el log si es necesario
    # ---------------------------------------------------------------
    top_cls = payload.get("top_class")
    confianza = payload.get("top_prob")

    if not top_cls or confianza is None:
        log_path = payload.get("log_path")
        if log_path:
            logger.info("[WS-INGEST] top_class/top_prob faltante. Leyendo log: %s", log_path)
            
            loop = asyncio.get_running_loop()
            
            # Ejecutar la lectura del archivo en un hilo separado para no bloquear el Event Loop
            log_content = await loop.run_in_executor(
                None, 
                _read_json_file_sync, 
                log_path
            )
            
            if log_content:
                # Calcular la clase y confianza máxima del archivo
                extracted_top_cls, extracted_confianza = _extract_top_class_and_prob(log_content)
                
                # Sobrescribir solo si se extrajo algo válido
                if extracted_top_cls and extracted_confianza is not None:
                    top_cls = extracted_top_cls
                    confianza = extracted_confianza
                    logger.info("[WS-INGEST] Confianza y clase extraídas del log: %s, %.2f", top_cls, confianza)

    # ---------------------------------------------------------------
    # 2. Continuar con la lógica de creación del evento
    # ---------------------------------------------------------------
    async with session_factory() as session:
        # Repos
        clip_repo = ClipRepository(session)
        evento_repo = EventoRepository(session)
        # Services (EventoService necesita clip_repo)
        clip_service = ClipService(clip_repo)
        evento_service = EventoService(evento_repo, clip_repo)

        # Duración (seg)
        # ... (código existente para calcular start, end, duration_sec) ...
        from datetime import datetime
        def parse_iso(s: str) -> datetime:
            # tolera 'Z'
            return datetime.fromisoformat(s.replace("Z", "+00:00"))

        start = parse_iso(payload["event_start_time"])
        end = parse_iso(payload["event_end_time"])
        duration_sec = max(0, int((end - start).total_seconds()))
        
        # 1) Crear Clip
        clip = await clip_service.create_clip(
            id_conexion=id_conexion,
            storage_path=payload["video_path"],
            start_time_utc=start,
            duration_sec=duration_sec,
        )

        # 2) Tipo de evento (usando el top_cls encontrado o extraído)
        tipo_evento = _to_tipo_evento(top_cls) # Usa el valor extraído o el original (None)

        # 3) Normalizar confianza (usando el valor extraído o el original)
        if isinstance(confianza, (int, float)):
            confianza = max(0.0, min(1.0, float(confianza)))
        else:
            confianza = None

        # 4) Crear Evento (USANDO CONFIANZA Y TIPO_EVENTO CORREGIDOS)
        evento = await evento_service.create_evento(
            id_conexion=id_conexion,
            id_clip=clip.id,
            tipo_evento=tipo_evento,
            confianza=confianza, # <-- ¡YA NO DEBERÍA SER NULL!
            t_inicio_ms=0,
            t_fin_ms=duration_sec * 1000,
            timestamp_evento=start,
            subclip_path=payload["log_path"],
            subclip_duracion_sec=duration_sec,
            procesado=False,
        )

        # ... (resto de la lógica de notificación) ...
        # (El resto del código dentro del async with session_factory() se mantiene igual)
        try:
            from app.survillance.infrastructure.repositories import NotificacionRepository
            from app.survillance.application.services.notificacion_service import NotificacionService
            from app.survillance.application.dto import NotificacionCreate

            notif_repo = NotificacionRepository(session)
            notif_service = NotificacionService(notif_repo)
            
            notif_msg = _build_sms_body(
                tipo_evento=tipo_evento,
                confianza=confianza,
                camera_id="cam_01",
                fecha_evento=start,
            )

            canal = "app"
            destinatario = f"usuario:{id_conexion}"

            notif = await notif_service.create(
                NotificacionCreate(
                    mensaje=notif_msg,
                    canal=canal,
                    destinatario="usuario:1",
                )
            )

            sms_body = notif_msg  # reutilizamos el mismo mensaje

            sms_result: TwilioSmsResult = await sms_service.send_alert_sms(
                sms_body,
                max_retries=1,  # 1 intento extra (total 2 envíos)
            )

        except Exception as e:
            logger.warning("[WS-INGEST] No se pudo crear notificación: %s", e)

        await session.commit()
        logger.info("[WS-INGEST] Evento creado id=%s, clip id=%s", evento.id, clip.id)
        return {"id_evento": evento.id, "id_clip": clip.id}
# ... importaciones y definiciones (WsIngestSettings, _to_tipo_evento, _create_clip_and_event) ...

# --- NUEVA FUNCIÓN: Manejar mensajes de predicción intermedia ---
async def _handle_prediction_message(
    *,
    payload: dict,
    id_conexion: int,
    session_factory: Callable,
):
    """
    Maneja el mensaje de predicción intermedia (e.g., cuando triggered=True).
    Aquí puedes implementar la lógica de notificación en tiempo real o caching.
    payload esperado:
        { type: "prediction", camera_id, triggered, probabilities: {cls: prob}, ... }
    """
    if not payload.get("triggered"):
        return # Ignorar si no superó el umbral

    camera_id = payload.get("camera_id")
    probabilities = payload.get("probabilities", {})
    
    # 1. Obtener la clase y probabilidad con mayor confianza
    if not probabilities:
        return
    
    top_class = max(probabilities, key=probabilities.get)
    top_prob = probabilities[top_class]
    
    # 2. Definir el tipo de evento preliminar y la confianza
    tipo_evento = _to_tipo_evento(top_class)
    confianza = max(0.0, min(1.0, float(top_prob)))
    
    logger.info(
        "[WS-INGEST] Predicción recibida: Cam %s, Evento: %s, Confianza: %.2f",
        camera_id,
        tipo_evento.value,
        confianza
    )

    # 3. Lógica de tu Backend (ejemplo: enviar notificación preliminar, guardar en caché, etc.)
    # Aquí puedes usar la confianza y el tipo_evento para decidir qué tipo de notificación enviar.
    # Por ejemplo, si confianza > 0.8, enviar una notificación "ALERTA CRÍTICA".

    try:
        # Ejemplo: Enviar Notificación Preliminar (Asumiendo que tienes un DTO/Servicio similar)
        # Nota: La lógica de la notificación se deja como ejemplo y debe adaptarse a tu
        # implementación actual (usando el session_factory).
        async with session_factory() as session:
            # Importaciones deben estar al inicio del archivo, pero se repiten aquí por claridad.
            from app.survillance.infrastructure.repositories import NotificacionRepository
            from app.survillance.application.services.notificacion_service import NotificacionService
            from app.survillance.application.dto import NotificacionCreate

            notif_repo = NotificacionRepository(session)
            notif_service = NotificacionService(notif_repo)
            
            mensaje = f"[PRE-ALERTA] Posible {tipo_evento.value} detectado. Confianza: {confianza:.2f}"
            canal = "app_pre"
            destinatario = f"conexion:{id_conexion}"

            await notif_service.create(
                NotificacionCreate(
                    mensaje=mensaje,
                    canal=canal,
                    destinatario="usuario:1",
                )
            )
            await session.commit()
            logger.info("[WS-INGEST] Notificación preliminar enviada para Cam %s.", camera_id)

    except Exception as e:
        logger.warning("[WS-INGEST] No se pudo crear notificación preliminar: %s", e)


# --- Función modificada para escuchar y procesar ambos tipos de mensajes ---
async def _listen_one_camera(
    *,
    camera_id: str,
    id_conexion: int,
    settings: WsIngestSettings,
    session_factory: Callable,
):
    """Mantiene una conexión WS a /ws/{camera_id} y procesa mensajes."""
    url = f"{settings.model_ws_base}/ws/{camera_id}"
    backoff = settings.reconnect_initial_ms

    while True:
        try:
            logger.info("[WS-INGEST] Conectando a %s ...", url)
            async with websockets.connect(url, max_size=8 * 1024 * 1024) as ws:
                logger.info("[WS-INGEST] Conectado a %s", url)
                backoff = settings.reconnect_initial_ms  # reset

                async for raw in ws:
                    try:
                        data = json.loads(raw)
                        if not isinstance(data, dict):
                            continue
                    except Exception:
                        continue

                    msg_type = data.get("type")
                    
                    if msg_type == "event_complete":
                        # Solo nos importa el mensaje final del evento
                        if not data.get("video_path") or not data.get("log_path"):
                            logger.warning("[WS-INGEST] event_complete sin paths: %s", data)
                            continue

                        try:
                            # Lógica para crear Clip y Evento (TU LÓGICA EXISTENTE)
                            await _create_clip_and_event(
                                payload=data,
                                id_conexion=id_conexion,
                                session_factory=session_factory,
                            )
                        except Exception as e:
                            logger.exception("[WS-INGEST] Error creando Clip/Evento: %s", e)
                            
                    elif msg_type == "prediction" and data.get("triggered"):
                        # NUEVA LÓGICA: Manejar predicciones intermedias que superaron el umbral
                        try:
                            await _handle_prediction_message(
                                payload=data,
                                id_conexion=id_conexion,
                                session_factory=session_factory,
                            )
                        except Exception as e:
                            logger.exception("[WS-INGEST] Error manejando predicción: %s", e)

        except Exception as e:
            logger.warning("[WS-INGEST] WS %s caído: %s", url, e)
            await asyncio.sleep(backoff / 1000.0)
            backoff = min(backoff * 2, settings.reconnect_max_ms)

async def run_ws_event_consumer(*, session_factory: Callable, settings: Optional[WsIngestSettings] = None):
    """
    Arranca 1 tarea por cámara y se mantiene vivo.
    Invócalo en on_startup de FastAPI: asyncio.create_task(run_ws_event_consumer(...))
    """
    settings = settings or WsIngestSettings.from_env()
    if not settings.cameras:
        logger.warning("[WS-INGEST] Sin cámaras configuradas (MODEL_CAMERAS vacío).")
        return

    tasks = []
    for cam in settings.cameras:
        conn_id = settings.conexion_by_camera.get(cam)
        if not conn_id:
            logger.warning("[WS-INGEST] camera_id %s sin id_conexion mapeado. Omitiendo.", cam)
            continue
        tasks.append(
            asyncio.create_task(
                _listen_one_camera(
                    camera_id=cam,
                    id_conexion=conn_id,           # ← usar mapping (no hardcode)
                    settings=settings,
                    session_factory=session_factory,
                )
            )
        )

    logger.info("[WS-INGEST] Suscriptores iniciados para: %s", ", ".join(settings.cameras))
    await asyncio.gather(*tasks)
