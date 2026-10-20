from fastapi import APIRouter


router = APIRouter

@router.get("/inscricoes")
def criar_inscricao():
    
    return {
        "mensagem": "Inscrição recebida"
    }