"""
Schemas Pydantic para validação e serialização dos dados.
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


# -----------------------------------------------------------------------------
# Departamento
# -----------------------------------------------------------------------------

class DepartamentoBase(BaseModel):
    sigaa_id: int = Field(..., description="ID interno do SIGAA")
    nome: str = Field(..., description="Nome do departamento")


class DepartamentoResponse(DepartamentoBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# -----------------------------------------------------------------------------
# Professor
# -----------------------------------------------------------------------------

class ProfessorBase(BaseModel):
    nome: str = Field(..., description="Nome completo do docente")


class ProfessorResponse(ProfessorBase):
    id: int
    departamento_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# -----------------------------------------------------------------------------
# Turma
# -----------------------------------------------------------------------------

class TurmaBase(BaseModel):
    codigo: str = Field(..., description="Código da turma (ex: 01)")
    ano_periodo: str = Field(..., description="Ano e período (ex: 2026.2)")
    horario: Optional[str] = Field(None, description="Horário das aulas")
    local: Optional[str] = Field(None, description="Local das aulas")
    vagas_ofertadas: Optional[int] = Field(None, description="Quantidade de vagas ofertadas")
    vagas_ocupadas: Optional[int] = Field(None, description="Quantidade de vagas ocupadas")


class TurmaResponse(TurmaBase):
    id: int
    disciplina_id: int
    professores: list[ProfessorResponse] = []
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# -----------------------------------------------------------------------------
# Disciplina
# -----------------------------------------------------------------------------

class DisciplinaEquivalente(BaseModel):
    codigo: str = Field(..., description="Código da disciplina equivalente (ex: CIC0088)")
    nome: Optional[str] = Field(None, description="Nome da disciplina equivalente")


class DisciplinaBase(BaseModel):
    codigo: str = Field(..., description="Código da disciplina (ex: CIC0004)")
    nome: str = Field(..., description="Nome da disciplina")
    tipo: Optional[str] = Field(None, description="Tipo: DISCIPLINA, ATIVIDADE, BLOCO, MÓDULO")
    nivel: Optional[str] = Field(None, description="Nível de ensino")
    carga_horaria: Optional[int] = Field(None, description="Carga horária total")
    pre_requisitos: Optional[str] = Field(None, description="Expressão de pré-requisitos")
    co_requisitos: Optional[str] = Field(None, description="Expressão de co-requisitos")
    equivalencias: Optional[str] = Field(None, description="Expressão de equivalências ativas")
    ementa: Optional[str] = Field(None, description="Ementa oficial")


class DisciplinaResponse(DisciplinaBase):
    id: int
    departamento_id: Optional[int] = None
    professores: list[ProfessorResponse] = []
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class DisciplinaComDepartamento(DisciplinaResponse):
    departamento: Optional[DepartamentoResponse] = None
    turmas: list[TurmaResponse] = []
    disciplinas_equivalentes: list[DisciplinaEquivalente] = Field(
        default_factory=list, description="Lista de disciplinas equivalentes identificadas"
    )


class ProfessorComDisciplinas(ProfessorResponse):
    departamento: Optional[DepartamentoResponse] = None
    disciplinas: list[DisciplinaBase] = []


# -----------------------------------------------------------------------------
# Scraping
# -----------------------------------------------------------------------------

class ScrapingRequest(BaseModel):
    nivel: str = Field(
        default="G",
        description="Nível de ensino: G=Graduação, S=Stricto Sensu, L=Lato Sensu, F=Formação Complementar",
    )
    departamento_sigaa_id: Optional[int] = Field(
        673, description="ID SIGAA do departamento (ex: 673 = UnB Campus Gama, 508 = Computação, ou null para todos)"
    )
    tipo: Optional[int] = Field(
        default=2, description="Tipo: 2=DISCIPLINA, 1=ATIVIDADE, 4=BLOCO, 3=MÓDULO"
    )
    buscar_professores: bool = Field(
        default=True, description="Se True, também busca as turmas e professores no SIGAA"
    )
    ano: Optional[str] = Field(
        default=None, description="Ano letivo (ex: '2026'). Se omitido, usa o padrão do SIGAA"
    )
    periodo: Optional[str] = Field(
        default=None, description="Período letivo (ex: '1', '2'). Se omitido, usa o padrão do SIGAA"
    )


class ScrapingLogResponse(BaseModel):
    id: int
    departamento_sigaa_id: Optional[int] = None
    nivel: Optional[str] = None
    status: str
    disciplinas_encontradas: int
    disciplinas_novas: int
    disciplinas_atualizadas: int
    professores_encontrados: int = 0
    turmas_encontradas: int = 0
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
    total_professores: int
    total_turmas: int
    disciplinas_por_nivel: dict
    ultimo_scraping: Optional[ScrapingLogResponse] = None
