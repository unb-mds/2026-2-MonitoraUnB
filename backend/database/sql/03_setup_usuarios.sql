CREATE ROLE monitora_app LOGIN;

GRANT USAGE ON SCHEMA public TO monitora_app;

-- permissões das tabelas
GRANT SELECT, INSERT ON TABLE public.aluno TO monitora_app;
GRANT SELECT ON TABLE public.disciplina TO monitora_app;
GRANT SELECT, INSERT ON TABLE public.inscricao TO monitora_app;
GRANT SELECT, UPDATE ON TABLE public.processo_seletivo TO monitora_app;
GRANT SELECT, INSERT, UPDATE ON TABLE public.resultado TO monitora_app;
GRANT SELECT ON TABLE public.usuario_administrador TO monitora_app;

-- permissões das sequências
GRANT SELECT, USAGE ON SEQUENCE public.aluno_id_aluno_seq TO monitora_app;
GRANT SELECT, USAGE ON SEQUENCE public.disciplina_id_disciplina_seq TO monitora_app;
GRANT SELECT, USAGE ON SEQUENCE public.inscricao_id_inscricao_seq TO monitora_app;
GRANT SELECT, USAGE ON SEQUENCE public.processo_seletivo_id_processo_seq TO monitora_app;
GRANT SELECT, USAGE ON SEQUENCE public.resultado_id_resultado_seq TO monitora_app;
GRANT SELECT, USAGE ON SEQUENCE public.usuario_administrador_id_usuario_seq TO monitora_app;

-- permissões das views
GRANT SELECT ON TABLE public.vw_inscricoes_pendentes TO monitora_app;
GRANT SELECT ON TABLE public.vw_ranking_geral TO monitora_app;
GRANT SELECT ON TABLE public.vw_ranking_por_disciplina TO monitora_app;
GRANT SELECT ON TABLE public.vw_total_inscritos_disciplina TO monitora_app;
