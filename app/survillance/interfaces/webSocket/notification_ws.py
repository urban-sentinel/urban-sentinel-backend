from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from app.survillance.application.services.notification_ws_manager import manager

router = APIRouter()

@router.websocket("/ws/notifications")
async def notifications_ws(
    websocket: WebSocket,
    destinatario: str,  # p.e. "conexion:1"
    # token: str = Query(None)  # si quieres validar JWT
):
    await manager.connect(destinatario, websocket)
    try:
        while True:
            # No esperamos nada del cliente; solo para que la conexión no muera
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(destinatario, websocket)