import math

from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks

from sqlalchemy.orm import Session

from backend.database.database import get_db
from backend.database.models import Departamento, Disciplina
from backend.schemas.schemas import DepartamentoResponse, DisciplinaResponse
from backend.scraping.sigaa import sincronizar_departamentos


router = APIRouter(
    prefix="/departamentos",
    tags=["Departamentos"]
)

@router.get("")
def listar_departamentos(db: Session = Depends(get_db)):
    """Lista todos os departamentos/unidades acadêmicas cadastrados."""
    return db.query(Departamento).order_by(Departamento.nome).all()


@router.get("/{depto_id}/disciplinas", response_model=dict)
def disciplinas_por_departamento(
    depto_id: int,
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    """Lista todas as disciplinas de um departamento específico."""
    departamento = db.query(Departamento).filter_by(id=depto_id).first()
    if not departamento:
        raise HTTPException(status_code=404, detail="Departamento não encontrado")

    query = db.query(Disciplina).filter_by(departamento_id=depto_id)
    total = query.count()
    pages = math.ceil(total / per_page) if total > 0 else 1

    disciplinas = (
        query.order_by(Disciplina.codigo)
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
    )

    return {
        "departamento": DepartamentoResponse.model_validate(departamento),
        "total": total,
        "page": page,
        "per_page": per_page,
        "pages": pages,
        "items": [DisciplinaResponse.model_validate(d) for d in disciplinas],
    }


@router.post("/sincronizar")
def sync_departamentos(db: Session = Depends(get_db)):
    """Sincroniza a lista de departamentos do SIGAA no banco de dados."""
    count = sincronizar_departamentos(db)
    return {"message": f"{count} departamentos sincronizados", "total": count}


