
"""python setup_db.py"""

import sys
import pymysql

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from app.config import get_settings
from app.database import init_db
from app.scraper import sincronizar_departamentos
from app.database import SessionLocal

settings = get_settings()


def criar_banco_de_dados():
    """Cria o banco de dados se for MySQL e ainda não existir."""
    if not settings.DATABASE_URL.startswith("mysql"):
        print(f"banco de dados SQLite ({settings.DATABASE_URL})...")
        return

    print(f"Conectando ao MySQL em {settings.DB_HOST}:{settings.DB_PORT}...")
    try:
        conn = pymysql.connect(
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
        )
        cursor = conn.cursor()
        cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS `{settings.DB_NAME}` "
            f"CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
        )
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Banco de dados '{settings.DB_NAME}' criado/verificado com sucesso!")
    except pymysql.Error as e:
        print(f"Erro ao criar banco de dados MySQL: {e}")
        sys.exit(1)


def criar_tabelas():
    """Cria todas as tabelas definidas nos modelos."""
    print("Criando tabelas...")
    init_db()

    # Garantir colunas novas nas tabelas existentes
    from sqlalchemy import text
    from app.database import engine
    with engine.connect() as conn:
        for col in ["professores_encontrados", "turmas_encontradas"]:
            try:
                conn.execute(text(f"ALTER TABLE scraping_logs ADD COLUMN {col} INTEGER DEFAULT 0"))
                conn.commit()
            except Exception:
                pass  # Coluna já existe

        for col in ["pre_requisitos", "co_requisitos", "equivalencias", "ementa"]:
            try:
                conn.execute(text(f"ALTER TABLE disciplinas ADD COLUMN {col} TEXT"))
                conn.commit()
            except Exception:
                pass  # Coluna já existe

    print("Tabelas criadas com sucesso!")


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
    print("  SIGAA UnB - Setup do Banco de Dados")
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
