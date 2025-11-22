from collections import defaultdict
from typing import Dict, List
from fastapi import WebSocket
import json

class NotificationWSManager:
    def __init__(self) -> None:
        self.connections: Dict[str, List[WebSocket]] = defaultdict(list)

    async def connect(self, destinatario: str, ws: WebSocket):
        await ws.accept()
        self.connections[destinatario].append(ws)

    def disconnect(self, destinatario: str, ws: WebSocket):
        conns = self.connections.get(destinatario)
        if not conns:
            return
        if ws in conns:
            conns.remove(ws)
        if not conns:
            self.connections.pop(destinatario, None)

    async def send_to_destinatario(self, destinatario: str, payload: dict):
        """Envía la notificación a todos los clientes suscritos a ese destinatario."""
        conns = list(self.connections.get(destinatario, []))
        dead: List[WebSocket] = []
        for ws in conns:
            try:
                await ws.send_json(payload)
            except Exception:
                # conexión rota
                dead.append(ws)
        for ws in dead:
            self.disconnect(destinatario, ws)

manager = NotificationWSManager()