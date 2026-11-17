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

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def main() -> int:
    senha = getpass("Senha do professor: ")
    confirma = getpass("Confirme a senha: ")

    if not senha:
        print("Erro: senha vazia.", file=sys.stderr)
        return 1

    if senha != confirma:
        print("Erro: as senhas não coincidem.", file=sys.stderr)
        return 1

    # bcrypt limita a 72 bytes; avisa se a senha for maior
    if len(senha.encode("utf-8")) > 72:
        print(
            "Erro: a senha excede 72 bytes (limite do bcrypt).",
            file=sys.stderr,
        )
        return 1

    hash_gerado = pwd_context.hash(senha)
    print()
    print("Cole no .env:")
    print(f"PROFESSOR_PASSWORD_HASH={hash_gerado}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
