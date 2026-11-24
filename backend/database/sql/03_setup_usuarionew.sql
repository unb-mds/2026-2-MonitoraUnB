-- =====================================================================
-- 03_setup_usuario.sql — papéis e permissões da aplicação e do scraper.
-- Executar com um superusuário/dono do schema, DEPOIS do 01_schema.sql.
-- =====================================================================

-- Cria o papel somente se ainda não existir (script pode ser reexecutado).
-- A senha NÃO fica neste arquivo. Defina depois, em outra consulta:
--     ALTER ROLE monitora_app PASSWORD 'defina-uma-senha-forte';
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'monitora_app') THEN
        CREATE ROLE monitora_app LOGIN;
    END IF;
END
$$;

GRANT USAGE ON SCHEMA public TO monitora_app;

-- ---------------------------------------------------------------------
-- Tabelas
-- ---------------------------------------------------------------------
GRANT SELECT, INSERT         ON TABLE public.aluno                 TO monitora_app;
GRANT SELECT                 ON TABLE public.disciplina            TO monitora_app;
GRANT SELECT, INSERT         ON TABLE public.inscricao             TO monitora_app;
-- INSERT em processo_seletivo: necessário para o app criar processos.
-- Remova se os processos forem criados fora da aplicação.
GRANT SELECT, INSERT, UPDATE ON TABLE public.processo_seletivo     TO monitora_app;
GRANT SELECT, INSERT, UPDATE ON TABLE public.resultado             TO monitora_app;
GRANT SELECT                 ON TABLE public.usuario_administrador TO monitora_app;

-- ---------------------------------------------------------------------
-- Sequências
-- ---------------------------------------------------------------------
-- Nenhum GRANT é necessário: todas as chaves são GENERATED ALWAYS AS IDENTITY,
-- e quem faz o INSERT só precisa de INSERT na tabela (não da sequência).

-- ---------------------------------------------------------------------
-- Views
-- ---------------------------------------------------------------------
GRANT SELECT ON TABLE public.vw_inscricoes_pendentes       TO monitora_app;
GRANT SELECT ON TABLE public.vw_ranking_geral              TO monitora_app;
GRANT SELECT ON TABLE public.vw_ranking_por_disciplina     TO monitora_app;
GRANT SELECT ON TABLE public.vw_total_inscritos_disciplina TO monitora_app;

-- ---------------------------------------------------------------------
-- Função de limpeza (SECURITY DEFINER): só o app pode executar
-- ---------------------------------------------------------------------
REVOKE ALL ON FUNCTION public.limpar_processo_encerrado(integer) FROM PUBLIC;
GRANT EXECUTE ON FUNCTION public.limpar_processo_encerrado(integer) TO monitora_app;

-- ---------------------------------------------------------------------
-- Scraper do SIGAA: papel separado, com acesso só à tabela disciplina
-- (princípio do menor privilégio: o scraper não enxerga alunos nem notas).
-- Defina a senha depois, em outra consulta:
--     ALTER ROLE monitora_scraper PASSWORD 'defina-uma-senha-forte';
-- Se preferir que o scraper use o monitora_app, troque o papel nos GRANTs
-- abaixo e apague este bloco de CREATE ROLE.
-- ---------------------------------------------------------------------
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'monitora_scraper') THEN
        CREATE ROLE monitora_scraper LOGIN;
    END IF;
END
$$;

GRANT USAGE ON SCHEMA public TO monitora_scraper;

-- INSERT + UPDATE permitem upsert por (codigo, semestre) (INSERT ... ON CONFLICT (codigo, semestre)
-- DO UPDATE); SELECT é exigido pelo ON CONFLICT DO UPDATE.
GRANT SELECT, INSERT, UPDATE ON TABLE public.disciplina TO monitora_scraper;
