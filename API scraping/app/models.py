"""
Modelos SQLAlchemy para o banco de dados.
"""

from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
    UniqueConstraint,
    Index,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


# Tabela associativa entre Disciplina e Professor (Muitos-para-Muitos)
disciplina_professores = Table(
    "disciplina_professores",
    Base.metadata,
    Column("disciplina_id", Integer, ForeignKey("disciplinas.id", ondelete="CASCADE"), primary_key=True),
    Column("professor_id", Integer, ForeignKey("professores.id", ondelete="CASCADE"), primary_key=True),
)

# Tabela associativa entre Turma e Professor (Muitos-para-Muitos)
turma_professores = Table(
    "turma_professores",
    Base.metadata,
    Column("turma_id", Integer, ForeignKey("turmas.id", ondelete="CASCADE"), primary_key=True),
    Column("professor_id", Integer, ForeignKey("professores.id", ondelete="CASCADE"), primary_key=True),
)


class Departamento(Base):
    """Unidade acadêmica / departamento da UnB."""

    __tablename__ = "departamentos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    sigaa_id = Column(Integer, unique=True, nullable=False, comment="ID interno do SIGAA")
    nome = Column(String(300), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relacionamento com disciplinas e professores
    disciplinas = relationship("Disciplina", back_populates="departamento")
    professores = relationship("Professor", back_populates="departamento")

    def __repr__(self):
        return f"<Departamento(sigaa_id={self.sigaa_id}, nome='{self.nome}')>"


class Professor(Base):
    """Docente/Professor da UnB."""

    __tablename__ = "professores"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(300), nullable=False, unique=True, index=True, comment="Nome completo do docente")
    departamento_id = Column(Integer, ForeignKey("departamentos.id"), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relacionamentos
    departamento = relationship("Departamento", back_populates="professores")
    disciplinas = relationship(
        "Disciplina",
        secondary=disciplina_professores,
        back_populates="professores",
    )
    turmas = relationship(
        "Turma",
        secondary=turma_professores,
        back_populates="professores",
    )

    def __repr__(self):
        return f"<Professor(id={self.id}, nome='{self.nome}')>"


class Turma(Base):
    """Turma de um componente curricular ofertada em determinado ano/período."""

    __tablename__ = "turmas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    codigo = Column(String(20), nullable=False, comment="Código da turma (ex: 01)")
    ano_periodo = Column(String(20), nullable=False, comment="Ano e período (ex: 2026.2)")
    horario = Column(String(500), nullable=True, comment="Horário das aulas")
    local = Column(String(300), nullable=True, comment="Local das aulas")
    vagas_ofertadas = Column(Integer, nullable=True)
    vagas_ocupadas = Column(Integer, nullable=True)
    disciplina_id = Column(Integer, ForeignKey("disciplinas.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relacionamentos
    disciplina = relationship("Disciplina", back_populates="turmas")
    professores = relationship(
        "Professor",
        secondary=turma_professores,
        back_populates="turmas",
    )

    __table_args__ = (
        UniqueConstraint("disciplina_id", "codigo", "ano_periodo", name="uq_turma_periodo"),
    )

    def __repr__(self):
        return f"<Turma(codigo='{self.codigo}', ano_periodo='{self.ano_periodo}')>"


class Disciplina(Base):
    """Componente curricular (disciplina) da UnB."""

    __tablename__ = "disciplinas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    codigo = Column(String(20), nullable=False, index=True, comment="Código da disciplina (ex: CIC0004)")
    nome = Column(String(300), nullable=False, comment="Nome da disciplina")
    tipo = Column(String(50), nullable=True, comment="Tipo: DISCIPLINA, ATIVIDADE, BLOCO, MÓDULO")
    nivel = Column(String(50), nullable=True, comment="Nível de ensino: GRADUAÇÃO, STRICTO SENSU, etc.")
    carga_horaria = Column(Integer, nullable=True, comment="Carga horária total em horas")
    departamento_id = Column(Integer, ForeignKey("departamentos.id"), nullable=True)
    pre_requisitos = Column(Text, nullable=True, comment="Expressão de pré-requisitos")
    co_requisitos = Column(Text, nullable=True, comment="Expressão de co-requisitos")
    equivalencias = Column(Text, nullable=True, comment="Expressão de equivalências")
    ementa = Column(Text, nullable=True, comment="Ementa oficial do componente")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relacionamentos
    departamento = relationship("Departamento", back_populates="disciplinas")
    professores = relationship(
        "Professor",
        secondary=disciplina_professores,
        back_populates="disciplinas",
    )
    turmas = relationship(
        "Turma",
        back_populates="disciplina",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        UniqueConstraint("codigo", "nivel", name="uq_codigo_nivel"),
        Index("idx_nome", "nome"),
    )

    def __repr__(self):
        return f"<Disciplina(codigo='{self.codigo}', nome='{self.nome}')>"


class ScrapingLog(Base):
    """Log de execuções do scraper para rastreabilidade."""

    __tablename__ = "scraping_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    departamento_sigaa_id = Column(Integer, nullable=True)
    nivel = Column(String(50), nullable=True)
    status = Column(String(20), nullable=False, comment="SUCCESS, ERROR, RUNNING")
    disciplinas_encontradas = Column(Integer, default=0)
    disciplinas_novas = Column(Integer, default=0)
    disciplinas_atualizadas = Column(Integer, default=0)
    professores_encontrados = Column(Integer, default=0)
    turmas_encontradas = Column(Integer, default=0)
    mensagem = Column(Text, nullable=True)
    started_at = Column(DateTime, server_default=func.now())
    finished_at = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<ScrapingLog(id={self.id}, status='{self.status}')>"
