"""
Schemas Pydantic para validação dos dados.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# Departamento

class DepartamentoBase(BaseModel):
    sigaa_id: int = Field(..., description="ID interno do SIGAA")
    nome: str = Field(..., description="Nome do departamento")


class DepartamentoResponse(DepartamentoBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Disciplina
class DisciplinaBase(BaseModel):
    codigo: str = Field(..., description="Código da disciplina (ex: CIC0004)")
    nome: str = Field(..., description="Nome da disciplina")
    tipo: Optional[str] = Field(None, description="Tipo: DISCIPLINA, ATIVIDADE, BLOCO, MÓDULO")
    nivel: Optional[str] = Field(None, description="Nível de ensino")
    carga_horaria: Optional[int] = Field(None, description="Carga horária total")


class DisciplinaResponse(DisciplinaBase):
    id: int
    departamento_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class DisciplinaComDepartamento(DisciplinaResponse):
    departamento: Optional[DepartamentoResponse] = None


# Scraping

class ScrapingRequest(BaseModel):
    nivel: str = Field(
        default="G",
        description="Nível de ensino: G=Graduação, S=Stricto Sensu, L=Lato Sensu, F=Formação Complementar",
    )
    departamento_sigaa_id: Optional[int] = Field(
        673, description="ID SIGAA do departamento (ex: 673 = UnB Campus Gama, 518 = Matemática, ou null para todos)"
    )
    tipo: Optional[int] = Field(
        default=2, description="Tipo: 2=DISCIPLINA, 1=ATIVIDADE, 4=BLOCO, 3=MÓDULO"
    )


class ScrapingLogResponse(BaseModel):
    id: int
    departamento_sigaa_id: Optional[int] = None
    nivel: Optional[str] = None
    status: str
    disciplinas_encontradas: int
    disciplinas_novas: int
    disciplinas_atualizadas: int
    mensagem: Optional[str] = None
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ScrapingStatusResponse(BaseModel):
    status: str
    message: str
    log: Optional[ScrapingLogResponse] = None


class PaginatedResponse(BaseModel):
    total: int
    page: int
    per_page: int
    pages: int
    items: list


class EstatisticasResponse(BaseModel):
    total_disciplinas: int
    total_departamentos: int
    disciplinas_por_nivel: dict
    ultimo_scraping: Optional[ScrapingLogResponse] = None
