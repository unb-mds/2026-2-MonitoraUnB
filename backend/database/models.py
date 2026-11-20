"""
Modelos SQLAlchemy correspondentes às tabelas PostgreSQL do projeto.
"""

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    text,
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

    disciplinas = relationship("Disciplina", back_populates="departamento")

    def __repr__(self):
        return f"<Departamento(sigaa_id={self.sigaa_id}, nome='{self.nome}')>"


class Disciplina(Base):
    """Componente curricular (disciplina) da UnB."""

    __tablename__ = "disciplina"

    # Mantém o atributo Python id usado pelas rotas e schemas,
    # mapeando-o para a coluna PostgreSQL id_disciplina.
    id = Column("id_disciplina", Integer, primary_key=True, autoincrement=True)
    codigo = Column(String(30), nullable=False, comment="Código da disciplina (ex: CIC0004)")
    nome = Column(String(300), nullable=False, comment="Nome da disciplina")
    tipo = Column(String(50), nullable=True, comment="Tipo: DISCIPLINA, ATIVIDADE, BLOCO, MÓDULO")
    nivel = Column(String(50), nullable=True, comment="Nível de ensino: GRADUAÇÃO, STRICTO SENSU, etc.")
    carga_horaria = Column(Integer, nullable=True, comment="Carga horária total em horas")
    departamento_id = Column(Integer, ForeignKey("departamentos.id"), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    departamento = relationship("Departamento", back_populates="disciplinas")

    __table_args__ = (
        UniqueConstraint("codigo", name="disciplina_codigo_key"),
    )

    def __repr__(self):
        return f"<Disciplina(codigo='{self.codigo}', nome='{self.nome}')>"


class Aluno(Base):
    """Estudante associado a uma ou mais inscrições."""

    __tablename__ = "aluno"

    id_aluno = Column(Integer, primary_key=True, autoincrement=True)
    matricula = Column(String(9), nullable=False)
    nome = Column(String(150), nullable=False)
    email = Column(String(150), nullable=False)

    __table_args__ = (
        CheckConstraint("matricula ~ '^[0-9]{9}$'", name="chk_matricula"),
        UniqueConstraint("matricula", name="aluno_matricula_key"),
    )


class UsuarioAdministrador(Base):
    """Conta administrativa associada à abertura do processo seletivo."""

    __tablename__ = "usuario_administrador"

    id_usuario = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(150), nullable=False)
    senha_hash = Column(Text, nullable=False)
    ativo = Column(Boolean, nullable=False, default=True, server_default=text("true"))

    __table_args__ = (
        UniqueConstraint("email", name="uq_usuario_admin_email"),
    )


class ProcessoSeletivo(Base):
    """Processo de seleção de monitoria de um semestre."""

    __tablename__ = "processo_seletivo"

    id_processo = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(
        Integer,
        ForeignKey("usuario_administrador.id_usuario"),
        nullable=False,
    )
    semestre = Column(String(20), nullable=False)
    data_abertura = Column(Date, nullable=False)
    data_encerramento = Column(Date, nullable=False)
    status = Column(
        String(20),
        nullable=False,
        default="AGENDADO",
        server_default=text("'AGENDADO'"),
    )

    inscricoes = relationship("Inscricao", back_populates="processo")

    __table_args__ = (
        UniqueConstraint("semestre", name="uq_processo_seletivo"),
        CheckConstraint(
            "data_encerramento >= data_abertura",
            name="chk_datas_processo",
        ),
        CheckConstraint(
            "status IN ('AGENDADO', 'ABERTO', 'ENCERRADO')",
            name="chk_status_processo",
        ),
    )


class Inscricao(Base):
    """Candidatura de um aluno a uma disciplina em um processo seletivo."""

    __tablename__ = "inscricao"

    id_inscricao = Column(Integer, primary_key=True, autoincrement=True)
    id_aluno = Column(
        Integer,
        ForeignKey("aluno.id_aluno", ondelete="CASCADE"),
        nullable=False,
    )
    id_disciplina = Column(
        Integer,
        ForeignKey("disciplina.id_disciplina"),
        nullable=False,
    )
    id_processo = Column(
        Integer,
        ForeignKey("processo_seletivo.id_processo", ondelete="CASCADE"),
        nullable=False,
    )
    ira = Column(Numeric(4, 2), nullable=False)
    mencao = Column(String(2), nullable=False)
    coeficiente = Column(Numeric(4, 2), nullable=False)
    data_inscricao = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )

    aluno = relationship("Aluno")
    disciplina = relationship("Disciplina")
    processo = relationship("ProcessoSeletivo", back_populates="inscricoes")

    __table_args__ = (
        UniqueConstraint("id_aluno", "id_processo", name="uq_aluno_processo"),
    )


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
