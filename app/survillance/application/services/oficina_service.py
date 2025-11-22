"""
Servicio CRUD de oficinas.
"""
from typing import List

from fastapi import HTTPException, status

from app.shared.time import now_utc
from app.survillance.domain.entities.office import Oficina
from app.survillance.domain.repositories_interfaces import IOficinaRepository
from app.survillance.application.dto import OficinaCreate, OficinaUpdate


class OficinaService:
    """Servicio CRUD de oficinas"""
    
    def __init__(self, oficina_repo: IOficinaRepository):
        self.oficina_repo = oficina_repo
    
    async def create(self, data: OficinaCreate) -> Oficina:
        """Crea una oficina"""
        oficina = Oficina(
            nombre_oficina=data.nombre_oficina,
            direccion=data.direccion,
            ciudad=data.ciudad,
            responsable=data.responsable,
            telefono_contacto=data.telefono_contacto,
            fecha_registro=now_utc()
        )
        return await self.oficina_repo.create(oficina)
    
    async def get_by_id(self, id_oficina: int) -> Oficina:
        """Obtiene oficina por ID"""
        oficina = await self.oficina_repo.get_by_id(id_oficina)
        if not oficina:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Oficina no encontrada"
            )
        return oficina
    
    async def get_all(self, limit: int = 100, offset: int = 0) -> List[Oficina]:
        """Lista todas las oficinas"""
        return await self.oficina_repo.get_all(limit, offset)
    
    async def update(self, id_oficina: int, data: OficinaUpdate) -> Oficina:
        """Actualiza una oficina"""
        oficina = await self.get_by_id(id_oficina)
        
        if data.nombre_oficina is not None:
            oficina.nombre_oficina = data.nombre_oficina
        if data.direccion is not None:
            oficina.direccion = data.direccion
        if data.ciudad is not None:
            oficina.ciudad = data.ciudad
        if data.responsable is not None:
            oficina.responsable = data.responsable
        if data.telefono_contacto is not None:
            oficina.telefono_contacto = data.telefono_contacto
        
        return await self.oficina_repo.update(oficina)
    
    async def delete(self, id_oficina: int) -> bool:
        """Elimina una oficina"""
        return await self.oficina_repo.delete(id_oficina)

