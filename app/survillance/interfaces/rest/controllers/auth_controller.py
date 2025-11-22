"""
Controlador de autenticación: registro, login, refresh.
"""
from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.shared.db import get_session
from app.survillance.infrastructure.repositories import UsuarioRepository
from app.survillance.application.services.auth_service import AuthService
from app.survillance.application.dto import *
from app.shared.security import decode_token

from fastapi import HTTPException, status, Query

router = APIRouter(prefix="/api/auth", tags=["Autenticación"])

@router.get("/users", response_model=list[UserResponse])
async def get_users(
    email: str | None = Query(
        default=None,
        description="Email del usuario a buscar. Si no se envía, devuelve todos."
    ),
    session: AsyncSession = Depends(get_session),
):
    """
    GET /users
        - /users               → lista todos los usuarios
        - /users?email=algo@x.com → devuelve solo el usuario con ese email
    """
    user_repo = UsuarioRepository(session)
    auth_service = AuthService(user_repo)

    # Si viene email → buscamos solo ese
    if email is not None:
        usuario = await auth_service.get_by_email(email)

        if usuario is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado",
            )

        # devolvemos una lista con 1 elemento para respetar el response_model
        return [UserResponse.model_validate(usuario)]

    # Si NO viene email → devolvemos todos
    usuarios = await auth_service.get_all_users()
    return [UserResponse.model_validate(u) for u in usuarios]

@router.post("/register", response_model=TokenResponse, status_code=201)
async def register(
    data: RegisterRequest,
    session: AsyncSession = Depends(get_session)
):
    """Registra un nuevo usuario"""
    user_repo = UsuarioRepository(session)
    auth_service = AuthService(user_repo)
    
    usuario = await auth_service.register(data)
    
    # Generar token automáticamente
    token_response = await auth_service.login(
        LoginRequest(email=data.email, password=data.password)
    )
    
    return token_response


@router.post("/login", response_model=TokenResponse)
async def login(
    data: LoginRequest,
    session: AsyncSession = Depends(get_session)
):
    """Autentica un usuario y retorna JWT"""
    user_repo = UsuarioRepository(session)
    auth_service = AuthService(user_repo)
    
    return await auth_service.login(data)


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    data: RefreshRequest,
    session: AsyncSession = Depends(get_session)
):
    """Refresca un token JWT"""
    user_repo = UsuarioRepository(session)
    auth_service = AuthService(user_repo)
    
    return await auth_service.refresh(data)

@router.delete("/users", status_code=204)
async def delete_user(
    id: int = Query(..., gt=0),
    session: AsyncSession = Depends(get_session)
):
    """Elimina un usuario por ID"""
    user_repo = UsuarioRepository(session)
    auth_service = AuthService(user_repo)

    await auth_service.delete_by_id(id)

@router.post("/change-password", status_code=204)
async def change_password(
    data: ChangePasswordRequest,
    session: AsyncSession = Depends(get_session)
):
    """Cambia la contraseña de un usuario"""
    user_repo = UsuarioRepository(session)
    auth_service = AuthService(user_repo)
    await auth_service.change_password(data)

@router.post("/forgot-password", status_code=204)
async def forgot_password(
    data: ForgotPasswordRequest,
    session: AsyncSession = Depends(get_session)
):
    """Inicia el proceso de recuperación de contraseña"""
    user_repo = UsuarioRepository(session)
    auth_service = AuthService(user_repo)
    await auth_service.request_password_reset(data.email)

@router.get("/reset-password/validate", status_code=204)
async def validate_reset_password_token(token: str):
    """
    Valida si el token de reseteo es válido y no ha expirado.
    No devuelve body, solo 204 si es válido, 400 si no.
    """
    decode_token(token)
    return Response(status_code=204)