"""
Schemas da API de consulta e sincronização dos dados do SIGAA.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class SchemaORM(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class DepartamentoResponse(SchemaORM):
    id: int
    sigaa_id: int
    nome: str
    created_at: datetime | None = None
    updated_at: datetime | None = None


class ProfessorResponse(SchemaORM):
    id: int
    nome: str
    departamento_id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class TurmaResponse(SchemaORM):
    id: int
    codigo: str
    ano_periodo: str
    horario: str | None = None
    local: str | None = None
    vagas_ofertadas: int | None = None
    vagas_ocupadas: int | None = None
    disciplina_id: int
    professores: list[ProfessorResponse] = Field(default_factory=list)
    created_at: datetime | None = None
    updated_at: datetime | None = None


class DisciplinaEquivalente(BaseModel):
    codigo: str
    nome: str | None = None


class DisciplinaResumo(BaseModel):
    codigo: str
    nome: str
    tipo: str | None = None
    nivel: str | None = None
    carga_horaria: int | None = None


class DisciplinaResponse(SchemaORM):
    id: int
    codigo: str
    nome: str
    tipo: str | None = None
    nivel: str | None = None
    carga_horaria: int | None = None
    departamento_id: int | None = None
    pre_requisitos: str | None = None
    co_requisitos: str | None = None
    equivalencias: str | None = None
    ementa: str | None = None
    professores: list[ProfessorResponse] = Field(default_factory=list)
    created_at: datetime | None = None
    updated_at: datetime | None = None


class DisciplinaComDepartamento(DisciplinaResponse):
    departamento: DepartamentoResponse | None = None
    turmas: list[TurmaResponse] = Field(default_factory=list)
    disciplinas_equivalentes: list[DisciplinaEquivalente] = Field(
        default_factory=list,
    )


class ProfessorComDisciplinas(ProfessorResponse):
    departamento: DepartamentoResponse | None = None
    disciplinas: list[DisciplinaResumo] = Field(default_factory=list)


class ScrapingRequest(BaseModel):
    nivel: str = Field(
        default="G",
        description="G=Graduação, S=Stricto Sensu, L=Lato Sensu, F=Formação Complementar",
    )
    departamento_sigaa_id: int | None = Field(
        default=None,
        description="ID SIGAA do departamento; null solicita todos.",
    )
    tipo: int | None = Field(
        default=2,
        description="2=DISCIPLINA, 1=ATIVIDADE, 4=BLOCO, 3=MÓDULO",
    )
    buscar_professores: bool = True
    ano: str | None = None
    periodo: str | None = None


class ScrapingLogResponse(SchemaORM):
    id: int
    departamento_sigaa_id: int | None = None
    nivel: str | None = None
    status: str
    disciplinas_encontradas: int = 0
    disciplinas_novas: int = 0
    disciplinas_atualizadas: int = 0
    professores_encontrados: int = 0
    turmas_encontradas: int = 0
    mensagem: str | None = None
    started_at: datetime | None = None
    finished_at: datetime | None = None


class ScrapingStatusResponse(BaseModel):
    status: str
    message: str
    log: ScrapingLogResponse | None = None


class EstatisticasResponse(BaseModel):
    total_disciplinas: int
    total_departamentos: int
    total_professores: int
    total_turmas: int
    disciplinas_por_nivel: dict[str, int]
    ultimo_scraping: ScrapingLogResponse | None = None
