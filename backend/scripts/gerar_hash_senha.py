"""Gera um hash bcrypt para PROFESSOR_PASSWORD_HASH e atualiza o arquivo .env.

Uso (na raiz do repositório, com o venv ativo e as deps instaladas):

    python backend/scripts/gerar_hash_senha.py

Não versionar o arquivo .env nem a senha em texto puro.
"""

from __future__ import annotations

from getpass import getpass
from pathlib import Path
import sys
import bcrypt


def atualizar_env(caminho_env: Path, chave: str, valor: str) -> None:
  """Atualiza a chave no .env se ela já existir, ou adiciona no final."""
  linha_nova = f"{chave}={valor}\n"

  if not caminho_env.exists():
    caminho_env.write_text(linha_nova, encoding="utf-8")
    return

  linhas = caminho_env.read_text(encoding="utf-8").splitlines(keepends=True)
  encontrou = False

  for i, linha in enumerate(linhas):
    if linha.lstrip().startswith(f"{chave}="):
      linhas[i] = linha_nova
      encontrou = True
      break

  if not encontrou:
    if linhas and not linhas[-1].endswith("\n"):
      linhas[-1] += "\n"
    linhas.append(linha_nova)

  caminho_env.write_text("".join(linhas), encoding="utf-8")


def main() -> int:
  senha = getpass("Senha do professor: ")
  confirma = getpass("Confirme a senha: ")

  if not senha:
    print("Erro: senha vazia.", file=sys.stderr)
    return 1

  if senha != confirma:
    print("Erro: as senhas não coincidem.", file=sys.stderr)
    return 1

  senha_bytes = senha.encode("utf-8")

  if len(senha_bytes) > 72:
    print(
        "Erro: a senha excede 72 bytes (limite do bcrypt).",
        file=sys.stderr,
    )
    return 1

  hash_gerado = bcrypt.hashpw(senha_bytes, bcrypt.gensalt()).decode("utf-8")

  # Escapa $ para $$ para o Docker Compose não expandir $2b e $12
  hash_para_env = hash_gerado.replace("$", "$$")

  caminho_env = Path(".env")
  atualizar_env(caminho_env, "PROFESSOR_PASSWORD_HASH", hash_para_env)

  print("Sucesso: PROFESSOR_PASSWORD_HASH atualizado no arquivo .env.")
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
