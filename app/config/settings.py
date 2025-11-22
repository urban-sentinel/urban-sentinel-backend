"""
Configuración centralizada de la aplicación usando pydantic-settings.
"""
from __future__ import annotations

import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# === Localiza el .env ===
# Este archivo está en app/config/settings.py → la raíz es dos niveles arriba.
ROOT_DIR = Path(__file__).resolve().parents[2]

# Usa APP_ENV=development|staging|production (por defecto: development)
APP_ENV = os.getenv("APP_ENV", "development")

# Si hay .env.<APP_ENV> lo usamos; si no, .env
ENV_PATH = ROOT_DIR / f".env.{APP_ENV}"
if not ENV_PATH.exists():
    ENV_PATH = ROOT_DIR / ".env"

# (Opcional) ayuda para detectar problemas rápido
assert ENV_PATH.exists(), f"No se encontró archivo de entorno: {ENV_PATH}"

class Settings(BaseSettings):
    """Configuración global de la aplicación"""

    # Database
    DATABASE_URL: str

    # JWT
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRES_MIN: int = 6000

    # Opcional
    IA_BASE_URL: str = ""
    WEBHOOK_SECRET: str = ""

    FRONTEND_BASE_URL: str = "http://localhost:5173"

    TWILIO_ACCOUNT_SID: str = "REEMPLAZA"
    TWILIO_AUTH_TOKEN: str = "REEMPLAZA"
    TWILIO_FROM_NUMBER: str = "REEMPLAZA"
    TWILIO_DEFAULT_TO_NUMBER: str = "REEMPLAZA"

    model_config = SettingsConfigDict(
        env_file=str(ENV_PATH),      # ← aquí el archivo dinámico
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

settings = Settings()
