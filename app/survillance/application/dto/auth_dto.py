"""
DTOs for authentication.
"""
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class RegisterRequest(BaseModel):
    """Request for user registration"""
    nombre: str = Field(..., max_length=100)
    apellido: str | None = Field(None, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=2)
    rol: str | None = Field(None, max_length=60)
    phone: str | None = None


class LoginRequest(BaseModel):
    """Request for login"""
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Response with JWT tokens"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class RefreshRequest(BaseModel):
    """Request for refresh token"""
    token: str


class UserResponse(BaseModel):
    """Response with user information"""
    id: int = Field(alias="id_usuario")
    nombre: str
    apellido: str | None = None
    email: EmailStr
    rol: str | None = None
    phone: str | None = None

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )

class ChangePasswordRequest(BaseModel):
    email: EmailStr
    current_password: str
    new_password: str

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ValidateTokenRequest(BaseModel):
    token: str

class DeleteUserRequest(BaseModel):
    id: int