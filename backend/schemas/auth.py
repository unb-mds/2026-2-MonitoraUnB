"""Schemas Pydantic para autenticação do professor."""

from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    username: str = Field(..., min_length=1, description="Login do professor")
    password: str = Field(..., min_length=1, description="Senha do professor")


class LoginResponse(BaseModel):
    mensagem: str
    username: str


class MeResponse(BaseModel):
    authenticated: bool
    username: str | None = None


class MensagemResponse(BaseModel):
    mensagem: str
