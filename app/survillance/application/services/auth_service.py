"""
Authentication and user management service.
"""
from fastapi import HTTPException, status

from app.shared.security import hash_password, verify_password, create_access_token
from app.shared.time import now_utc
from app.survillance.domain.entities.user import Usuario
from app.survillance.domain.repositories_interfaces import IUsuarioRepository
from app.survillance.application.dto import RegisterRequest, LoginRequest, TokenResponse, RefreshRequest, ChangePasswordRequest
from app.config.settings import settings
from app.shared.security import create_reset_token
from app.shared.services.email_service import send_email

class AuthService:
    """Authentication and user management service"""
    
    def __init__(self, user_repo: IUsuarioRepository):
        self.user_repo = user_repo
    
    async def request_password_reset(self, email: str) -> None:
        usuario = await self.user_repo.get_by_email(email)
        if not usuario:
            # No revelar si existe o no
            return

        token = create_reset_token(usuario.id)  # esto ya lo vimos antes
        reset_link = f"{settings.FRONTEND_BASE_URL}/reset-password?token={token}"

        html = f"""
            <h3>Recuperación de contraseña</h3>
            <p>Hola, {usuario.email if hasattr(usuario, "nombre") else "usuario"}.</p>
            <p>Has solicitado restablecer tu contraseña. Haz clic en el siguiente enlace:</p>
            <p><a href="{reset_link}">Restablecer contraseña</a></p>
            <p>Si no fuiste tú, puedes ignorar este correo.</p>
            """
        try:
            send_email(
                to_email=email,
                subject="Recuperación de contraseña",
                html_body=html,
            )
        except Exception as e:
            print("ERROR ENVIANDO EMAIL:", e)

    async def change_password(self, data: ChangePasswordRequest) -> None:
        user = await self.get_by_email(data.email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        if not verify_password(data.current_password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect"
            )
        
        if verify_password(data.new_password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="New password must be different from the current password"
            )
        
        user.password_hash = hash_password(data.new_password)
        await self.user_repo.update(user)

    async def get_all_users(self) -> list[Usuario]:
        """Gets all users"""
        return await self.user_repo.get_all()
    
    async def delete_by_id(self, id: int) -> None:
        """Deletes a user by ID"""
        await self.user_repo.delete_by_id(id)
    
    async def get_by_id(self, id: int) -> Usuario:
        """Gets a user by ID"""
        usuario = await self.user_repo.get_by_id(id)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return usuario
    
    async def get_by_email(self, email: str) -> Usuario:
        """Gets a user by email"""
        usuario = await self.user_repo.get_by_email(email)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return usuario

    async def register(self, data: RegisterRequest) -> Usuario:
        """Registers a new user"""
        existing = await self.user_repo.get_by_email(data.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email ya registrado"
            )
        # Create entity without id (autoincrement)
        userEntity = Usuario(
            nombre=data.nombre,
            email=data.email,
            password_hash=hash_password(data.password),
            apellido=data.apellido,
            rol=data.rol,
            phone=data.phone,
            fecha_creacion=now_utc(),
            # id=None (implicit, not passed)
            # ultimo_login=None (implicit, not passed)
        )
        usuario = await self.user_repo.create(userEntity)
        
        return usuario
    
    async def login(self, data: LoginRequest) -> TokenResponse:
        usuario = await self.user_repo.get_by_email(data.email)
        if not usuario or not verify_password(data.password, usuario.password_hash):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # Update last login
        usuario.ultimo_login = now_utc()
        usuario = await self.user_repo.update(usuario)

        # Use domain id (int)
        if usuario.id is None:
            raise HTTPException(status_code=500, detail="User without ID")
        token = create_access_token(usuario.id)

        # expires_in in seconds
        return TokenResponse(access_token=token, expires_in=settings.JWT_EXPIRES_MIN * 60)
    
    async def refresh(self, data: RefreshRequest) -> TokenResponse:
        """Refreshes a JWT token (simplified)"""
        # In production, implement separate refresh token
        token = create_access_token({"sub": 1})
        return TokenResponse(
            access_token=token,
            expires_in=settings.JWT_EXPIRES_MIN * 3600
        )
    