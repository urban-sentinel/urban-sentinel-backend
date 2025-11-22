from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from twilio.rest import Client

from app.config.settings import settings  # 👈 importa settings de tu app

router = APIRouter(prefix="/api/messages", tags=["Messages"])

# ====== CONFIG TWILIO ======
TWILIO_ACCOUNT_SID = settings.TWILIO_ACCOUNT_SID
TWILIO_AUTH_TOKEN = settings.TWILIO_AUTH_TOKEN
TWILIO_FROM_NUMBER = settings.TWILIO_FROM_NUMBER
TWILIO_DEFAULT_TO_NUMBER = settings.TWILIO_DEFAULT_TO_NUMBER  # puede ser None

twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


class AlertPayload(BaseModel):
    message: str
    phone_number: str | None = None  # si no viene, se usa TWILIO_DEFAULT_TO_NUMBER


@router.post("/alert")
async def send_twilio_alert(payload: AlertPayload):
    """
    Envía una alerta por SMS usando Twilio.

    - Si viene phone_number en el body, se usa ese.
    - Si no, se usa TWILIO_DEFAULT_TO_NUMBER (por ejemplo el celular del operador).
    """
    to_number = payload.phone_number or TWILIO_DEFAULT_TO_NUMBER

    if not to_number:
        raise HTTPException(
            status_code=400,
            detail="No se especificó phone_number y no hay TWILIO_DEFAULT_TO_NUMBER en Settings",
        )

    try:
        msg = twilio_client.messages.create(
            body=payload.message,
            from_=TWILIO_FROM_NUMBER,
            to=to_number,
        )
        return {
            "sid": msg.sid,
            "to": to_number,
        }
    except Exception as e:
        print("Error Twilio:", e)
        raise HTTPException(status_code=500, detail="Error al enviar SMS con Twilio")
