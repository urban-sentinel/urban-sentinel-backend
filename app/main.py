"""
Main entry point for the FastAPI application.
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import asyncio
import os

from app.shared.db import engine, Base
from app.shared.db import AsyncSessionLocal
from app.survillance.ingestion.ws_event_consumer import run_ws_event_consumer, WsIngestSettings

from app.config.settings import settings
from app.survillance.ingestion.camera_supervisor import camera_supervisor
from app.survillance.ingestion.retention_job import retention_job

from app.survillance.interfaces.webSocket.notification_ws import router as notifications_ws_router

from app.config.settings import settings, APP_ENV
from fastapi.staticfiles import StaticFiles

import logging


# Import controllers
from app.survillance.interfaces.rest.controllers import (
    auth_controller,
    office_controller,
    conection_controller,
    clip_controller,
    events_controller,
    notification_controller,
    notification_controller,
    report_controller,
    inference_controller,
    admin_controller,
    messages_controller
)

def background_ws_event_consumer():
    cams = list(getattr(settings, "MODEL_CAMERAS", ["cam_01"]))
    cam_map = getattr(settings, "MODEL_CAMERA_MAP", {}) or {cid: 1 for cid in cams}  # fallback simple
    ws_settings = WsIngestSettings(
        model_ws_base=getattr(settings, "MODEL_WS_BASE", "ws://127.0.0.1:8010"),
        cameras=cams,
        conexion_by_camera=cam_map,
        reconnect_initial_ms=getattr(settings, "WS_RECONNECT_INITIAL_MS", 500),
        reconnect_max_ms=getattr(settings, "WS_RECONNECT_MAX_MS", 5000),
    )
    print(f"[WS-INGEST] base={ws_settings.model_ws_base} cams={ws_settings.cameras} map={ws_settings.conexion_by_camera}")

    ws_task = asyncio.create_task(
        run_ws_event_consumer(session_factory=AsyncSessionLocal, settings=ws_settings)
    )
    return ws_task

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle management"""
    print("Starting application...")

    # Base directories (from settings)
    os.makedirs(settings.STORAGE_BASE_PATH, exist_ok=True)
    os.makedirs(os.path.join(settings.STORAGE_BASE_PATH, "events"), exist_ok=True)
    os.makedirs(os.path.join(settings.STORAGE_BASE_PATH, "temp"), exist_ok=True)

    # Migrations / tables in dev
    if APP_ENV == "development":
        print("Development mode: creating tables...")
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("Tables created successfully")
    else:
        print(f"{APP_ENV} mode: using Alembic migrations")

    ws_task = background_ws_event_consumer()

    print("Application started successfully")
    try:
        yield
    finally:
        # Ordered shutdown
        print("Stopping application...")
        ws_task.cancel()
        try:
            await ws_task
        except asyncio.CancelledError:
            pass

        await camera_supervisor.stop_all()
        await retention_job.stop()
        print("Application stopped")



# Create FastAPI application
app = FastAPI(
    title="Security and Surveillance System",
    description="Backend for RTSP camera management, AI events and clip buffer",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    openapi_url="/openapi.json"
)


logging.basicConfig(
    level=logging.INFO,  # ⬅️ clave: mostrar INFO y superiores
    format="%(levelname)s:%(name)s:%(message)s",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,          # ok SIEMPRE que no uses "*"
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Range", "Accept-Ranges"],  # <- el <video> los necesita
)


# Register routers
app.include_router(auth_controller.router)
app.include_router(office_controller.router)
app.include_router(conection_controller.router)
app.include_router(clip_controller.router)
app.include_router(events_controller.router)
app.include_router(notification_controller.router)
app.include_router(report_controller.router)
app.include_router(inference_controller.router)
app.include_router(admin_controller.router)
app.include_router(messages_controller.router)
app.include_router(notifications_ws_router)

@app.get("/api/health")
async def health_check():
    """Health endpoint"""
    return {
        "status": "ok",
        "message": "Security and Surveillance System operational"
    }


@app.get("/")
async def root():
    """Redirects to documentation"""
    return {
        "message": "Security and Surveillance System API",
        "docs": "/docs",
        "health": "/api/health"
    }