#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."

umask 077

AZUL='\033[1;34m'
VERDE='\033[1;32m'
VERMELHO='\033[1;31m'
CINZA='\033[0;90m'
RESET='\033[0m'


# Cabeçalho do MonitoraUnB
cabecalho() {
    if [[ -t 1 ]]; then
        clear || true
    fi

    printf '%b' "$AZUL"

    cat <<'EOF'

 __  __             _ _
|  \/  | ___  _ __ (_) |_ ___  _ __ __ _
| |\/| |/ _ \| '_ \| | __/ _ \| '__/ _` |
| |  | | (_) | | | | | || (_) | | | (_| |
|_|  |_|\___/|_| |_|_|\__\___/|_|  \__,_|

EOF

    printf '%b' "$VERDE"

    cat <<'EOF'
 _   _       ____
| | | |_ __ | __ )
| | | | '_ \|  _ \
| |_| | | | |_) |
 \___/|_| |_|____/

EOF

    printf '%b' "$CINZA"
    echo "──────────────────────────────────────────"
    printf '%b' "$RESET"

    echo "  Sistema de Gerenciamento de Monitorias"
    echo "  Universidade de Brasília"
    echo "  MDS 2026.2 | Equipe G11"

    printf '%b' "$CINZA"
    echo "──────────────────────────────────────────"
    printf '%b' "$RESET"

    printf '\n%b  CONFIGURAÇÃO INICIAL DO SISTEMA%b\n\n' \
        "$AZUL" "$RESET"
}


# Mensagens do sistema
sucesso() {
    printf '%b[OK]%b %s\n' "$VERDE" "$RESET" "$1"
}


erro() {
    printf '%b[ERRO]%b %s\n' "$VERMELHO" "$RESET" "$1" >&2
    exit 1
}


# Cria o .env caso não exista
preparar_env() {
    if [[ ! -f .env ]]; then
        cp .env.example .env
        sucesso "Arquivo .env criado."
    fi

    chmod 600 .env
}


# Atualiza uma variável no .env
atualizar_env() {
    local chave="$1"
    local valor="$2"

    ENV_CHAVE="$chave" ENV_VALOR="$valor" ./.venv/bin/python - <<'PY'
import os
from pathlib import Path

caminho = Path(".env")
chave = os.environ["ENV_CHAVE"]
valor = os.environ["ENV_VALOR"]
linha_nova = f"{chave}={valor}\n"

if not caminho.exists():
    caminho.write_text(linha_nova, encoding="utf-8")
else:
    linhas = caminho.read_text(encoding="utf-8").splitlines(keepends=True)
    encontrou = False
    for i, linha in enumerate(linhas):
        if linha.startswith(f"{chave}="):
            linhas[i] = linha_nova
            encontrou = True
            break
    if not encontrou:
        if linhas and not linhas[-1].endswith("\n"):
            linhas[-1] += "\n"
        linhas.append(linha_nova)
    caminho.write_text("".join(linhas), encoding="utf-8")
PY
}

# Instala o bcrypt
instalar_dependencias() {
    printf '\n%bPreparando ambiente Python%b\n\n' "$AZUL" "$RESET"

    if ! command -v python3 >/dev/null 2>&1; then
        erro "Python3 não está instalado."
    fi

    # Cria o ambiente virtual
    if [[ ! -x .venv/bin/python ]]; then
        python3 -m venv .venv
        sucesso "Ambiente virtual criado."
    fi

    # Instala somente se necessário
    if ! .venv/bin/python -c "import bcrypt" 2>/dev/null; then

        echo "Instalando dependências do setup..."

        .venv/bin/python -m pip install \
            --disable-pip-version-check \
            --quiet \
            -r backend/requirements/setup.txt

        sucesso "Dependências instaladas."
    else
        sucesso "Dependências já instaladas."
    fi
}




# Configura as credenciais do professor
configurar_professor() {
    local usuario
    local hash

    read -rp "Usuário do professor [professor]: " usuario
    usuario="${usuario:-professor}"

    if [[ ! "$usuario" =~ ^[a-zA-Z0-9_.@-]+$ ]]; then
        erro "Usuário inválido."
    fi

    if ! ./.venv/bin/python backend/scripts/gerar_hash_senha.py >/dev/null; then
        erro "Não foi possível gerar a senha."
    fi

    hash=$(grep -E '^PROFESSOR_PASSWORD_HASH=' .env | tail -n 1 | cut -d'=' -f2-)

    if [[ ! "$hash" =~ ^\$\$2[aby]\$\$[0-9]{2}\$\$[./A-Za-z0-9]{53}$ ]]; then
        erro "Hash bcrypt inválido."
    fi

    atualizar_env PROFESSOR_USERNAME "$usuario"

    echo ""
    sucesso "Usuário configurado."
    sucesso "Senha protegida com sucesso."
}


# Configura a chave de sessão
configurar_sessao() {
    local session_secret

    session_secret=$(./.venv/bin/python -c "import secrets; print(secrets.token_hex(32))")

    atualizar_env SESSION_SECRET "$session_secret"

    sucesso "Chave de sessão configurada."
}


# Configura a senha inicial do banco, se necessário
configurar_banco() {
    local senha

    echo

    read -rsp "Senha do banco de dados (Enter para padrão): " senha
    echo

    if [[ -z "$senha" ]]; then

        if grep -Eq "^DB_PASSWORD=.+$" .env &&
           ! grep -q "^DB_PASSWORD=substitua_por_uma_senha_segura$" .env; then

            sucesso "Senha existente do banco mantida."

            return
        fi

        senha=$(./.venv/bin/python -c \
            "import secrets; print(secrets.token_hex(8))")

        sucesso "Senha padrão gerada automaticamente."

    else

        sucesso "Senha personalizada selecionada."

    fi

    atualizar_env DB_PASSWORD "$senha"

    sucesso "Senha do PostgreSQL configurada."
}


# Validação final
finalizar() {
    docker compose config --quiet || \
        erro "Configuração do Docker Compose inválida."

    sucesso "Docker Compose validado."

    printf '\n%b' "$CINZA"
    echo "──────────────────────────────────────────"
    printf '%b' "$RESET"

    printf '\n%bAMBIENTE CONFIGURADO COM SUCESSO!%b\n\n' \
        "$VERDE" "$RESET"

    echo "Para iniciar o MonitoraUnB, execute:"
    printf '\n%b  docker compose up -d%b\n\n' \
        "$AZUL" "$RESET"

    echo "Endereço do sistema:"
    printf '%b  http://localhost:3000/pages/inicio.html%b\n\n' \
        "$AZUL" "$RESET"
}


# Execução principal
main() {
    cabecalho
    instalar_dependencias
    preparar_env
    configurar_professor
    configurar_sessao
    configurar_banco
    finalizar
}

main "$@"
