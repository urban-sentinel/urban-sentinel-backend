# app/shared/infra/sms/twilio_sms_service.py
from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass
from typing import Optional

from twilio.rest import Client
from app.config.settings import settings

logger = logging.getLogger(__name__)


@dataclass
class TwilioSmsResult:
    to: str
    sid: Optional[str]
    success: bool
    error: Optional[Exception] = None


class TwilioSmsService:
    """
    Servicio para enviar SMS con Twilio, con reintentos.
    Lo puedes reutilizar desde cualquier parte de la app.
    """

    def __init__(self) -> None:
        self._client = Client(
            settings.TWILIO_ACCOUNT_SID,
            settings.TWILIO_AUTH_TOKEN,
        )
        self._from_number = settings.TWILIO_FROM_NUMBER
        self._default_to_number = settings.TWILIO_DEFAULT_TO_NUMBER

    async def send_alert_sms(
        self,
        body: str,
        to: Optional[str] = None,
        *,
        max_retries: int = 1,
    ) -> TwilioSmsResult:
        """
        Envía un SMS y hace hasta max_retries reintentos si falla.
        Devuelve un TwilioSmsResult con info de éxito/error.
        """
        dest = to or self._default_to_number
        if not dest:
            raise ValueError("No hay número de destino configurado para SMS")

        loop = asyncio.get_running_loop()
        last_exc: Optional[Exception] = None

        for attempt in range(max_retries + 1):
            try:
                msg = await loop.run_in_executor(
                    None,
                    lambda: self._client.messages.create(
                        body=body,
                        from_=self._from_number,
                        to=dest,
                    ),
                )
                logger.info(
                    "[TwilioSMS] SMS enviado a %s (sid=%s, intento=%s)",
                    dest,
                    msg.sid,
                    attempt + 1,
                )
                return TwilioSmsResult(to=dest, sid=msg.sid, success=True)

            except Exception as exc:
                last_exc = exc
                logger.warning(
                    "[TwilioSMS] Error enviando SMS (intento %s/%s): %s",
                    attempt + 1,
                    max_retries + 1,
                    exc,
                )

        # Si llegó aquí, fallaron todos los intentos
        return TwilioSmsResult(to=dest, sid=None, success=False, error=last_exc)


# instancia global reutilizable
sms_service = TwilioSmsService()
