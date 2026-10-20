from fastapi import APIRouter


router = APIRouter

@router.get("/disciplinas")
def listar_disciplinas():
    
    return {
        "disciplinas": []
    }