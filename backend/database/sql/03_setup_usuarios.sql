DO $$
BEGIN
    IF NOT EXISTS (
        SELECT FROM pg_catalog.pg_roles WHERE rolname = 'monitora_app'
    ) THEN
        CREATE ROLE monitora_app LOGIN;
    END IF;
END
$$;

-- Execute após aplicar as migrações do schema, incluindo 002_integrar_dados_scraping.sql.
-- Defina a senha do papel interativamente no psql com: \password monitora_app
-- O valor deve ser o mesmo configurado em DB_PASSWORD no .env.

GRANT USAGE ON SCHEMA public TO monitora_app;

-- permissões das tabelas
GRANT SELECT, INSERT ON TABLE public.aluno TO monitora_app;
GRANT SELECT, INSERT, UPDATE ON TABLE public.disciplina TO monitora_app;
GRANT SELECT, INSERT ON TABLE public.inscricao TO monitora_app;
GRANT SELECT, UPDATE ON TABLE public.processo_seletivo TO monitora_app;
GRANT SELECT, INSERT, UPDATE ON TABLE public.resultado TO monitora_app;
GRANT SELECT ON TABLE public.usuario_administrador TO monitora_app;

-- permissões para sincronização de dados do SIGAA
GRANT SELECT, INSERT, UPDATE ON TABLE public.departamentos TO monitora_app;
GRANT SELECT, INSERT, UPDATE ON TABLE public.professores TO monitora_app;
GRANT SELECT, INSERT, UPDATE ON TABLE public.turmas TO monitora_app;
GRANT SELECT, INSERT ON TABLE public.disciplina_professores TO monitora_app;
GRANT SELECT, INSERT ON TABLE public.turma_professores TO monitora_app;
GRANT SELECT, INSERT, UPDATE ON TABLE public.scraping_logs TO monitora_app;

-- permissões das sequências
GRANT SELECT, USAGE ON SEQUENCE public.aluno_id_aluno_seq TO monitora_app;
GRANT SELECT, USAGE ON SEQUENCE public.disciplina_id_disciplina_seq TO monitora_app;
GRANT SELECT, USAGE ON SEQUENCE public.inscricao_id_inscricao_seq TO monitora_app;
GRANT SELECT, USAGE ON SEQUENCE public.processo_seletivo_id_processo_seq TO monitora_app;
GRANT SELECT, USAGE ON SEQUENCE public.resultado_id_resultado_seq TO monitora_app;
GRANT SELECT, USAGE ON SEQUENCE public.usuario_administrador_id_usuario_seq TO monitora_app;
GRANT SELECT, USAGE ON SEQUENCE public.departamentos_id_seq TO monitora_app;
GRANT SELECT, USAGE ON SEQUENCE public.professores_id_seq TO monitora_app;
GRANT SELECT, USAGE ON SEQUENCE public.turmas_id_seq TO monitora_app;
GRANT SELECT, USAGE ON SEQUENCE public.scraping_logs_id_seq TO monitora_app;

-- permissões das views
GRANT SELECT ON TABLE public.vw_inscricoes_pendentes TO monitora_app;
GRANT SELECT ON TABLE public.vw_ranking_geral TO monitora_app;
GRANT SELECT ON TABLE public.vw_ranking_por_disciplina TO monitora_app;
GRANT SELECT ON TABLE public.vw_total_inscritos_disciplina TO monitora_app;
