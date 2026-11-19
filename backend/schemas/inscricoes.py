"""
Schemas para validação e envio de inscrições.
"""

from typing import Literal

from pydantic import BaseModel, Field


class DisciplinaValidada(BaseModel):
    codigo: str
    nome: str
    mencao: str
    situacao: str
    periodo: str
    coef_mencao: int


class DadosHistoricoAssinados(BaseModel):
    aluno: str
    matricula: str
    ira: float
    status: str
    disciplina: DisciplinaValidada
    coeficiente_candidatura: float


class InscricaoRequest(BaseModel):
    token_validacao: str = Field(..., min_length=1)
    semestre: str = Field(..., pattern=r"^\d{4}/[12]$")
    email: str = Field(
        ...,
        min_length=5,
        max_length=254,
        pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$",
    )
    professor: str | None = Field(default=None, max_length=150)
    declaracao_sem_outra_bolsa: Literal[True]


class InscricaoResponse(BaseModel):
    status: Literal["validada"]
    mensagem: str
    coeficiente_candidatura: float
