"""
Gera um hash bcrypt para PROFESSOR_PASSWORD_HASH no arquivo .env.

Uso (na raiz do repositório, com o venv ativo e as deps instaladas):

    python backend/scripts/gerar_hash_senha.py

Cole a linha impressa em PROFESSOR_PASSWORD_HASH no seu .env local.
Não versionar o arquivo .env nem a senha em texto puro.
"""

from __future__ import annotations

import sys
from getpass import getpass
#import re
import bcrypt


def main() -> int:
    # TESTE PARA CRIACAO DO HASH 
    # consiste em comentar a parte do usuario que vai para o setup.sh
    # Criar um login de acordo com o usuario com login e senha novas
#    usuario = input("Usuário do professor [professor]: ").strip()
#    usuario = usuario or "professor"

#    if not re.fullmatch(r"[a-zA-Z0-9_.@-]+", usuario):
#        print("Erro: usuário inválido.", file=sys.stderr)
#        return 1

    # Cria a senha desse novo usuario
    senha = getpass("Senha do professor: ")
    confirma = getpass("Confirme a senha: ")

    if not senha:
        print("Erro: senha vazia.", file=sys.stderr)
        return 1

    if senha != confirma:
        print("Erro: as senhas não coincidem.", file=sys.stderr)
        return 1

    senha_bytes = senha.encode("utf-8")

    # bcrypt limita a 72 bytes; avisa se a senha for maior
    if len(senha_bytes) > 72:
        print(
            "Erro: a senha excede 72 bytes (limite do bcrypt).",
            file=sys.stderr,
        )
        return 1

    hash_gerado = bcrypt.hashpw(senha_bytes, bcrypt.gensalt()).decode("utf-8")
    print(hash_gerado)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
