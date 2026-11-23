"""python setup_db.py"""

import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from backend.config import get_settings
from backend.database.database import init_db, SessionLocal, engine
from backend.services.scraping_service import sincronizar_departamentos

settings = get_settings()


def criar_banco_de_dados():
    """Garante que o banco de dados PostgreSQL exista e aplica os scripts SQL."""
    print(f"Conectando ao PostgreSQL: banco '{settings.DB_NAME}' em {settings.DB_HOST}:{settings.DB_PORT}")

    # Tenta criar o banco de dados se ainda não existir, conectando-se ao banco de manutenção padrão 'postgres'
    if not getattr(settings, "DATABASE_URL_OVERRIDE", None):
        try:
            import psycopg2
            from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

            conn = psycopg2.connect(
                host=settings.DB_HOST,
                port=settings.DB_PORT,
                user=settings.DB_USER,
                password=settings.DB_PASSWORD,
                dbname="postgres",
            )
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cur = conn.cursor()
            cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{settings.DB_NAME}';")
            if not cur.fetchone():
                print(f"Criando banco de dados '{settings.DB_NAME}' no PostgreSQL...")
                cur.execute(f'CREATE DATABASE "{settings.DB_NAME}";')
                print(f"Banco de dados '{settings.DB_NAME}' criado com sucesso!")
            cur.close()
            conn.close()
        except Exception:
            # Se não conseguir conectar ao banco 'postgres' padrão, continua normalmente
            pass

    executar_scripts_sql_postgresql()


def executar_scripts_sql_postgresql():
    """Aplica os scripts 01_schema.sql, 02_seed.sql e 03_setup_usuarios.sql no PostgreSQL."""
    sql_files = [
        ("01_schema.sql", "app/01_schema.sql"),
        ("02_seed.sql", "app/02_seed.sql"),
        ("03_setup_usuarios.sql", "app/03_setup_usuarios.sql"),
    ]

    print("Verificando e aplicando scripts SQL (schema, seed, usuarios)...")
    try:
        with engine.raw_connection() as raw_conn:
            with raw_conn.cursor() as cur:
                for nome, caminho in sql_files:
                    if not os.path.exists(caminho):
                        continue
                    with open(caminho, "r", encoding="utf-8") as f:
                        conteudo = f.read().strip()
                    if not conteudo:
                        continue

                    print(f"  -> Aplicando {nome}...")
                    try:
                        cur.execute(conteudo)
                        raw_conn.commit()
                        print(f"  [OK] {nome} aplicado com sucesso.")
                    except Exception as e:
                        raw_conn.rollback()
                        msg = str(e).strip()
                        if "already exists" in msg or "ja existe" in msg or "já existe" in msg:
                            print(f"  [INFO] {nome}: tabelas/objetos já existem no banco. Continuando...")
                        else:
                            print(f"  [AVISO] {nome}: {msg}")
    except Exception as e:
        print(f"  [AVISO] Nao foi possivel rodar scripts SQL automaticamente: {e}")


def criar_tabelas():
    """Cria todas as tabelas definidas nos modelos da API."""
    print("Criando tabelas da API...")
    init_db()

    # Garantir colunas novas nas tabelas existentes (migrações retrocompatíveis)
    from sqlalchemy import text
    with engine.connect() as conn:
        for col in ["professores_encontrados", "turmas_encontradas"]:
            try:
                conn.execute(text(f"ALTER TABLE scraping_logs ADD COLUMN {col} INTEGER DEFAULT 0"))
                conn.commit()
            except Exception:
                conn.rollback()

        colunas_disciplina = [
            ("tipo", "VARCHAR(50)"),
            ("nivel", "VARCHAR(50)"),
            ("carga_horaria", "INTEGER"),
            ("departamento_id", "INTEGER"),
            ("pre_requisitos", "TEXT"),
            ("co_requisitos", "TEXT"),
            ("equivalencias", "TEXT"),
            ("ementa", "TEXT"),
            ("created_at", "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"),
            ("updated_at", "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"),
        ]
        for col, tipo in colunas_disciplina:
            try:
                conn.execute(text(f"ALTER TABLE disciplina ADD COLUMN {col} {tipo}"))
                conn.commit()
            except Exception:
                conn.rollback()

    print("Tabelas configuradas com sucesso!")


def popular_departamentos():
    """Popula a tabela de departamentos com os dados do SIGAA."""
    print("Sincronizando departamentos...")
    db = SessionLocal()
    try:
        count = sincronizar_departamentos(db)
        print(f"{count} departamentos sincronizados!")
    finally:
        db.close()


if __name__ == "__main__":
    print("=" * 60)
    print("  SIGAA UnB - Setup do Banco de Dados (PostgreSQL)")
    print("=" * 60)
    print()

    criar_banco_de_dados()
    criar_tabelas()
    popular_departamentos()

    print()
    print("=" * 60)
    print("Setup concluído. Execute a API com:")
    print("uvicorn main:app --reload")
    print("=" * 60)
