"""
Servicio CRUD de notificaciones.
"""
from typing import List, Optional

from fastapi import HTTPException, status

from app.survillance.domain.entities.notification import Notificacion
from app.survillance.domain.repositories_interfaces import INotificacionRepository
from app.survillance.domain.enums import EstadoNotificacion
from app.survillance.application.dto import NotificacionCreate, NotificacionUpdate

from app.survillance.application.services.notification_ws_manager import manager

class NotificacionService:
    """Servicio CRUD de notificaciones"""
    
    def __init__(self, notif_repo: INotificacionRepository):
        self.notif_repo = notif_repo
    
    async def create(self, data: NotificacionCreate) -> Notificacion:
        """Crea una notificación"""
        notif = Notificacion(
            mensaje=data.mensaje,
            canal=data.canal,
            destinatario=data.destinatario,
            estado=EstadoNotificacion.PENDIENTE
        )
        notif_ws_manager = manager

        payload = {
                "id": notif.id,
                "mensaje": notif.mensaje,
                "canal": notif.canal,
                "destinatario": notif.destinatario,
                "estado": notif.estado,
                "fecha_envio": notif.fecha_envio
            }

        await notif_ws_manager.send_to_destinatario(destinatario=data.destinatario, payload=payload)
        
        return await self.notif_repo.create(notif)
    
    async def get_all(
        self,
        limit: int = 100,
        offset: int = 0
    ) -> List[Notificacion]:
        """Lista notificaciones"""
        return await self.notif_repo.get_all(limit, offset)
    
    async def update(
        self,
        id_notificacion: int,
        data: NotificacionUpdate
    ) -> Notificacion:
        """Actualiza notificación"""
        notif = await self.notif_repo.get_by_id(id_notificacion)
        if not notif:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Notificación no encontrada"
            )
        
        if data.estado is not None:
            # Convertir string a enum si es necesario
            notif.estado = EstadoNotificacion(data.estado) if isinstance(data.estado, str) else data.estado
        if data.fecha_envio is not None:
            notif.fecha_envio = data.fecha_envio
        
        return await self.notif_repo.update(notif)

