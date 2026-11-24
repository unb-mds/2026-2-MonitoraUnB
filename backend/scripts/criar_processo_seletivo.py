#!/usr/bin/env python3
"""
Script interativo para criação de processo seletivo no Monitora UnB.

Execução:
    python backend/scripts/criar_processo_seletivo.py
"""

from __future__ import annotations

import sys
from datetime import date, datetime
from getpass import getpass
from pathlib import Path

# Garante que a raiz do projeto esteja no sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from sqlalchemy.orm import Session, sessionmaker

from backend.config import get_settings
from backend.database.models import ProcessoSeletivo, UsuarioAdministrador


class Cores:
    """Cores ANSI para o terminal."""
    AZUL = "\033[1;34m"
    VERDE = "\033[1;32m"
    VERMELHO = "\033[1;31m"
    AMARELO = "\033[1;33m"
    CIANO = "\033[1;36m"
    CINZA = "\033[0;90m"
    NEGRITO = "\033[1m"
    RESET = "\033[0m"

    @classmethod
    def desativar(cls):
        cls.AZUL = cls.VERDE = cls.VERMELHO = cls.AMARELO = ""
        cls.CIANO = cls.CINZA = cls.NEGRITO = cls.RESET = ""


if not sys.stdout.isatty():
    Cores.desativar()


def exibir_banner() -> None:
    largura = 60
    print(f"\n{Cores.AZUL}{Cores.NEGRITO}" + "═" * largura)
    print("       MONITORA UNB — NOVO PROCESSO SELETIVO")
    print("═" * largura + f"{Cores.RESET}")
    print(f"{Cores.CINZA}Pressione Ctrl+C a qualquer momento para cancelar.{Cores.RESET}\n")


def conectar_banco() -> Session:
    """Conecta ao PostgreSQL pedindo credenciais administrativas sem salvá-las."""
    settings = get_settings()

    usuario = input("Usuário administrador do PostgreSQL [monitora]: ").strip() or "monitora"
    senha = getpass("Senha do usuário administrador do PostgreSQL: ")
    if not senha:
        print(
            f"{Cores.VERMELHO}✖ A senha do banco não pode ficar vazia."
            f"{Cores.RESET}\n"
        )
        sys.exit(1)

    # Prioriza localhost/127.0.0.1 quando executado no host (Windows/Linux fora do Docker)
    hosts_para_tentar = ["localhost", "127.0.0.1"]
    if settings.DB_HOST not in hosts_para_tentar:
        hosts_para_tentar.append(settings.DB_HOST)

    engine = None
    ultimo_erro = None

    print(f"{Cores.CINZA}Conectando ao banco de dados...{Cores.RESET}")

    for host in hosts_para_tentar:
        try:
            db_url = URL.create(
                drivername="postgresql+psycopg",
                username=usuario,
                password=senha,
                host=host,
                port=settings.DB_PORT,
                database=settings.DB_NAME,
            )

            eng = create_engine(
                db_url,
                pool_pre_ping=True,
                connect_args={"connect_timeout": 3},
            )
            with eng.connect() as conn:
                conn.execute(text("SELECT 1;"))
            engine = eng
            break
        except Exception as e:
            ultimo_erro = e

    if engine is None:
        print(f"{Cores.VERMELHO}✖ Erro ao conectar ao banco de dados:{Cores.RESET} {ultimo_erro}")
        print(f"\n{Cores.AMARELO}ℹ Certifique-se de que o Docker está rodando:{Cores.RESET}")
        print("  docker compose up -d db\n")
        sys.exit(1)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()


def obter_usuario_responsavel(db: Session) -> UsuarioAdministrador:
    """
    Recupera ou registra automaticamente o usuário administrador
    usando o nome e o hash da senha do professor configurados no .env.
    """
    settings = get_settings()
    username = settings.PROFESSOR_USERNAME or "professor"
    email = f"{username}@unb.br" if "@" not in username else username

    # Normaliza o hash caso tenha sido escapado com '$$' para o Docker Compose
    senha_hash = (settings.PROFESSOR_PASSWORD_HASH or "hash_provisorio").replace("$$", "$")

    admin = db.query(UsuarioAdministrador).first()
    if not admin:
        admin = UsuarioAdministrador(
            email=email,
            senha_hash=senha_hash,
            ativo=True,
        )
        db.add(admin)
        db.flush()

    return admin


def coletar_semestre(db: Session) -> str:
    print(f"{Cores.CIANO}{Cores.NEGRITO}[1/3] Semestre Letivo{Cores.RESET}")
    print(f"{Cores.CINZA}Formato esperado: AAAA/S (ex: 2026/2, 2027/1){Cores.RESET}")

    while True:
        semestre = input("Informe o semestre: ").strip()
        if not semestre:
            print(f"{Cores.VERMELHO}O semestre não pode ser vazio.{Cores.RESET}")
            continue

        if not re.fullmatch(r"\d{4}/[12]", semestre):
            print(
                f"{Cores.VERMELHO}Formato inválido. Use AAAA/1 ou AAAA/2, "
                f"por exemplo 2027/1.{Cores.RESET}"
            )
            continue

        existente = db.query(ProcessoSeletivo).filter(ProcessoSeletivo.semestre == semestre).first()
        if existente:
            print(f"{Cores.VERMELHO}✖ Já existe um processo para o semestre '{semestre}'.{Cores.RESET}")
            continue

        print(f"{Cores.VERDE}✔ Semestre válido:{Cores.RESET} {semestre}\n")
        return semestre


def coletar_data(rotulo: str, valor_padrao: date | None = None) -> date:
    dica = f" [padrão: {valor_padrao.strftime('%d/%m/%Y')}]" if valor_padrao else ""
    while True:
        entrada = input(f"{rotulo}{dica}: ").strip()
        if not entrada and valor_padrao:
            return valor_padrao

        if entrada.lower() in ("hoje", "today"):
            return date.today()

        for fmt in ("%d/%m/%Y", "%d-%m-%Y", "%Y-%m-%d"):
            try:
                return datetime.strptime(entrada, fmt).date()
            except ValueError:
                pass

        print(f"{Cores.VERMELHO}Formato inválido. Use DD/MM/AAAA (ex: 15/08/2026).{Cores.RESET}")


def coletar_periodo() -> tuple[date, date]:
    print(f"{Cores.CIANO}{Cores.NEGRITO}[2/3] Período de Inscrição{Cores.RESET}")
    hoje = date.today()

    while True:
        dt_abertura = coletar_data("Data de abertura (início das inscrições)", valor_padrao=hoje)
        dt_encerramento = coletar_data("Data de encerramento (fim das inscrições)")

        if dt_encerramento < dt_abertura:
            print(f"{Cores.VERMELHO}✖ O encerramento não pode ser antes da abertura.{Cores.RESET}\n")
            continue

        print(f"{Cores.VERDE}✔ Período definido:{Cores.RESET} {dt_abertura.strftime('%d/%m/%Y')} até {dt_encerramento.strftime('%d/%m/%Y')}\n")
        return dt_abertura, dt_encerramento


def coletar_status(db: Session) -> tuple[str, ProcessoSeletivo | None]:
    print(f"{Cores.CIANO}{Cores.NEGRITO}[3/3] Status Inicial{Cores.RESET}")
    print(f"  {Cores.NEGRITO}[1]{Cores.RESET} ABERTO   (Recebe inscrições imediatamente)")
    print(f"  {Cores.NEGRITO}[2]{Cores.RESET} AGENDADO (Aguardando período oficial - Padrão)")

    while True:
        opcao = input(f"Escolha o status [{Cores.NEGRITO}1-2{Cores.RESET}, padrão 2]: ").strip()
        if opcao in ("", "2"):
            status_escolhido = "AGENDADO"
        elif opcao == "1":
            status_escolhido = "ABERTO"
        else:
            print(f"{Cores.VERMELHO}Opção inválida. Escolha 1 ou 2.{Cores.RESET}")
            continue

        if status_escolhido == "ABERTO":
            processo_aberto = db.query(ProcessoSeletivo).filter(ProcessoSeletivo.status == "ABERTO").first()
            if processo_aberto:
                print(f"\n{Cores.AMARELO}⚠ O semestre '{processo_aberto.semestre}' já está com status 'ABERTO'.{Cores.RESET}")
                print("O banco permite apenas um processo aberto por vez:")
                print(f"  [1] Criar como AGENDADO (Recomendado)")
                print(f"  [2] Encerrar o anterior ('{processo_aberto.semestre}') e abrir este")

                resp = input("\nOpção [1/2, padrão 1]: ").strip()
                if resp == "2":
                    return "ABERTO", processo_aberto
                return "AGENDADO", None

        print(f"{Cores.VERDE}✔ Status selecionado:{Cores.RESET} {status_escolhido}\n")
        return status_escolhido, None


def main() -> int:
    exibir_banner()
    db = conectar_banco()

    try:
        # Vincula automaticamente ao professor do .env
        admin = obter_usuario_responsavel(db)

        semestre = coletar_semestre(db)
        dt_abertura, dt_encerramento = coletar_periodo()
        status_processo, proc_anterior = coletar_status(db)

        # Resumo final
        print(f"\n{Cores.CIANO}{Cores.NEGRITO}════════════════ RESUMO ════════════════{Cores.RESET}")
        print(f"  • Responsável:     {admin.email}")
        print(f"  • Semestre:        {semestre}")
        print(f"  • Início:          {dt_abertura.strftime('%d/%m/%Y')}")
        print(f"  • Término:         {dt_encerramento.strftime('%d/%m/%Y')}")
        print(f"  • Status:          {status_processo}")
        print(f"{Cores.CIANO}{Cores.NEGRITO}════════════════════════════════════════{Cores.RESET}\n")

        confirma = input(f"Confirmar criação? [{Cores.NEGRITO}S/n{Cores.RESET}]: ").strip().lower()
        if confirma not in ("", "s", "sim"):
            print(f"\n{Cores.AMARELO}Operação cancelada.{Cores.RESET}\n")
            return 0

        if proc_anterior:
            proc_anterior.status = "ENCERRADO"

        novo_processo = ProcessoSeletivo(
            id_usuario=admin.id_usuario,
            semestre=semestre,
            data_abertura=dt_abertura,
            data_encerramento=dt_encerramento,
            status=status_processo,
        )
        db.add(novo_processo)
        db.commit()
        db.refresh(novo_processo)

        print(f"\n{Cores.VERDE}{Cores.NEGRITO}✔ PROCESSO SELETIVO CRIADO COM SUCESSO! (ID: {novo_processo.id_processo}){Cores.RESET}\n")
        return 0

    except KeyboardInterrupt:
        print(f"\n\n{Cores.AMARELO}Cancelado pelo usuário.{Cores.RESET}\n")
        return 1
    finally:
        db.close()


if __name__ == "__main__":
    raise SystemExit(main())
