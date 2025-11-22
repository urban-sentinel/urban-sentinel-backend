"""
Value Objects para rutas de medios con validación.
"""
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class StoragePath:
    """Ruta de almacenamiento de clip"""
    value: str
    
    def __post_init__(self):
        if not self.value or not self.value.strip():
            raise ValueError("StoragePath no puede estar vacío")
        
        # Validar que tenga extensión .mp4
        if not self.value.lower().endswith('.mp4'):
            raise ValueError(f"StoragePath debe terminar en .mp4, recibido: {self.value}")
    
    def __str__(self) -> str:
        return self.value
    
    def exists(self) -> bool:
        """Verifica si el archivo existe en disco"""
        return Path(self.value).exists()
    
    def filename(self) -> str:
        """Retorna solo el nombre del archivo"""
        return Path(self.value).name


@dataclass(frozen=True)
class SubclipPath:
    """Ruta de subclip de evento"""
    value: str
    
    def __post_init__(self):
        if not self.value or not self.value.strip():
            raise ValueError("SubclipPath no puede estar vacío")
        
        # Validar que tenga extensión .mp4
        # if not self.value.lower().endswith('.mp4'): raise ValueError(f"SubclipPath debe terminar en .mp4, recibido: {self.value}")
    
    def __str__(self) -> str:
        return self.value
    
    def exists(self) -> bool:
        """Verifica si el archivo existe en disco"""
        return Path(self.value).exists()
    
    def filename(self) -> str:
        """Retorna solo el nombre del archivo"""
        return Path(self.value).name


@dataclass(frozen=True)
class SnapshotPath:
    """Ruta de snapshot/imagen de evento"""
    value: str
    
    def __post_init__(self):
        if not self.value or not self.value.strip():
            raise ValueError("SnapshotPath no puede estar vacío")
        
        # Validar que tenga extensión de imagen
        valid_extensions = ('.jpg', '.jpeg', '.png', '.webp')
        if not any(self.value.lower().endswith(ext) for ext in valid_extensions):
            raise ValueError(
                f"SnapshotPath debe terminar en {valid_extensions}, recibido: {self.value}"
            )
    
    def __str__(self) -> str:
        return self.value
    
    def exists(self) -> bool:
        """Verifica si el archivo existe en disco"""
        return Path(self.value).exists()
    
    def filename(self) -> str:
        """Retorna solo el nombre del archivo"""
        return Path(self.value).name