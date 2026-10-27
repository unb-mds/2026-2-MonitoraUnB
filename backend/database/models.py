"""
Modelos SQLAlchemy para o banco de dados.
"""

from sqlalchemy import (
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

from backend.database.database import Base


class Departamento(Base):
    """Unidade acadêmica / departamento da UnB."""

    __tablename__ = "departamentos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    sigaa_id = Column(Integer, unique=True, nullable=False, comment="ID interno do SIGAA")
    nome = Column(String(300), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relacionamento com disciplinas
    disciplinas = relationship("Disciplina", back_populates="departamento")

    def __repr__(self):
        return f"<Departamento(sigaa_id={self.sigaa_id}, nome='{self.nome}')>"


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
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relacionamento com departamento
    departamento = relationship("Departamento", back_populates="disciplinas")

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
    mensagem = Column(Text, nullable=True)
    started_at = Column(DateTime, server_default=func.now())
    finished_at = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<ScrapingLog(id={self.id}, status='{self.status}')>"
