"""
Assinatura temporária dos dados acadêmicos já validados pelo histórico.
"""

from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from backend.config import get_settings
from backend.database.models import Aluno, Disciplina, Inscricao, ProcessoSeletivo
from backend.schemas.inscricoes import DadosHistoricoAssinados

TEMPO_MAXIMO_TOKEN_SEGUNDOS = 15 * 60
TOKEN_SALT = "monitoraunb-validacao-historico"
SEGREDO_LOCAL_DESENVOLVIMENTO = "dev-insecure-session-secret"


class DisciplinaNaoEncontradaError(Exception):
    """A disciplina do histórico ainda não está cadastrada no banco."""


class ProcessoNaoEncontradoError(Exception):
    """Não existe processo seletivo para o semestre solicitado."""


class ProcessoNaoAbertoError(Exception):
    """O processo seletivo existe, mas não está recebendo inscrições."""


class InscricaoDuplicadaError(Exception):
    """O aluno já possui inscrição no processo seletivo informado."""


def _serializador() -> URLSafeTimedSerializer:
    settings = get_settings()
    segredo = settings.SESSION_SECRET or SEGREDO_LOCAL_DESENVOLVIMENTO
    return URLSafeTimedSerializer(segredo, salt=TOKEN_SALT)


def gerar_token_validacao(dados: dict) -> str:
    """Assina os dados extraídos para que o frontend não possa alterá-los."""
    return _serializador().dumps(dados)


def ler_token_validacao(token: str) -> dict:
    """Valida a assinatura e a validade temporal do token recebido."""
    try:
        dados = _serializador().loads(
            token,
            max_age=TEMPO_MAXIMO_TOKEN_SEGUNDOS,
        )
    except SignatureExpired as erro:
        raise ValueError(
            "A validação do histórico expirou. Envie o histórico novamente."
        ) from erro
    except BadSignature as erro:
        raise ValueError(
            "O token de validação é inválido. Envie o histórico novamente."
        ) from erro

    if not isinstance(dados, dict):
        raise ValueError("O conteúdo do token de validação é inválido.")

    return dados


def registrar_inscricao(
    db: Session,
    historico: DadosHistoricoAssinados,
    semestre: str,
    email: str,
) -> Inscricao:
    """Localiza os registros relacionados e persiste a inscrição validada."""
    codigo_disciplina = historico.disciplina.codigo.strip().upper()
    disciplina = (
        db.query(Disciplina)
        .filter(Disciplina.codigo == codigo_disciplina)
        .first()
    )
    if disciplina is None:
        raise DisciplinaNaoEncontradaError

    # O bloqueio evita que o processo seja encerrado entre a consulta e a gravação.
    processo = (
        db.query(ProcessoSeletivo)
        .filter(ProcessoSeletivo.semestre == semestre)
        .with_for_update(read=True)
        .first()
    )
    if processo is None:
        raise ProcessoNaoEncontradoError
    if processo.status.strip().upper() != "ABERTO":
        raise ProcessoNaoAbertoError

    aluno_existente = (
        db.query(Aluno)
        .filter(Aluno.matricula == historico.matricula)
        .first()
    )
    if aluno_existente is not None:
        inscricao_existente = (
            db.query(Inscricao)
            .filter(
                Inscricao.id_aluno == aluno_existente.id_aluno,
                Inscricao.id_processo == processo.id_processo,
            )
            .first()
        )
        if inscricao_existente is not None:
            raise InscricaoDuplicadaError
        aluno = aluno_existente
    else:
        aluno = Aluno(
            matricula=historico.matricula,
            nome=historico.aluno,
            email=email,
        )
        db.add(aluno)

    inscricao = Inscricao(
        aluno=aluno,
        disciplina=disciplina,
        processo=processo,
        ira=historico.ira,
        mencao=historico.disciplina.mencao.strip().upper(),
        coeficiente=historico.coeficiente_candidatura,
    )
    db.add(inscricao)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()

        # A restrição do banco também protege contra duas requisições simultâneas.
        aluno_atual = (
            db.query(Aluno)
            .filter(Aluno.matricula == historico.matricula)
            .first()
        )
        if aluno_atual is not None:
            inscricao_atual = (
                db.query(Inscricao)
                .filter(
                    Inscricao.id_aluno == aluno_atual.id_aluno,
                    Inscricao.id_processo == processo.id_processo,
                )
                .first()
            )
            if inscricao_atual is not None:
                raise InscricaoDuplicadaError
        raise
    except SQLAlchemyError:
        db.rollback()
        raise

    return inscricao
