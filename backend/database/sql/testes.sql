-- =====================================================================
-- 99_testes.sql — verifica TODAS as regras do banco. Rodar num banco de
-- TESTE (nunca em produção), conectado como dono do banco (ex.: postgres),
-- depois de executar o 01_schema.sql e o 03_setup_usuario.sql.
--
-- COMO USAR NO pgAdmin: abra uma Query Tool no banco de teste, cole o
-- script inteiro (sem selecionar trecho) e execute. Veja a aba "Messages":
--   - "Regras do banco: OK" e "Permissões do monitora_app: OK" = passou.
--   - Se aparecer "TESTE FALHOU: ..." algo está errado. Como a execução
--     para no erro, execute depois a consulta:  ROLLBACK;
-- Tudo é desfeito no final (ROLLBACK): nada fica gravado no banco.
-- Obs.: não pode haver processo ABERTO no momento (só 1 por vez).
-- =====================================================================

BEGIN;

DO $$
DECLARE
    v_adm    integer;
    v_proc   integer;
    v_proc2  integer;
    v_disc   integer;
    v_disc2  integer;
    v_aluno  integer;
    v_insc   integer;
    v_res    integer;
    v_ok     boolean;
    n        integer;
BEGIN
    INSERT INTO usuario_administrador (email, senha_hash)
    VALUES ('teste-admin@teste.local', 'hash-de-teste')
    RETURNING id_usuario INTO v_adm;

    -- T1: processo não pode ser criado já ABERTO
    v_ok := false;
    BEGIN
        INSERT INTO processo_seletivo (id_usuario, semestre, data_abertura, data_encerramento, status)
        VALUES (v_adm, '9999/1', CURRENT_DATE, CURRENT_DATE, 'ABERTO');
    EXCEPTION WHEN OTHERS THEN v_ok := true;
    END;
    IF NOT v_ok THEN RAISE EXCEPTION 'TESTE FALHOU: T1 processo criado direto como ABERTO'; END IF;

    -- T2: formato de semestre inválido é recusado
    v_ok := false;
    BEGIN
        INSERT INTO processo_seletivo (id_usuario, semestre, data_abertura, data_encerramento)
        VALUES (v_adm, '9999.1', CURRENT_DATE, CURRENT_DATE);
    EXCEPTION WHEN OTHERS THEN v_ok := true;
    END;
    IF NOT v_ok THEN RAISE EXCEPTION 'TESTE FALHOU: T2 semestre com formato inválido aceito'; END IF;

    -- T3: criação normal (nasce AGENDADO)
    INSERT INTO processo_seletivo (id_usuario, semestre, data_abertura, data_encerramento)
    VALUES (v_adm, '9999/1', CURRENT_DATE, CURRENT_DATE + 30)
    RETURNING id_processo INTO v_proc;

    -- T4: não abre sem disciplinas do semestre
    v_ok := false;
    BEGIN
        UPDATE processo_seletivo SET status = 'ABERTO' WHERE id_processo = v_proc;
    EXCEPTION WHEN OTHERS THEN v_ok := true;
    END;
    IF NOT v_ok THEN RAISE EXCEPTION 'TESTE FALHOU: T4 abriu processo sem disciplinas'; END IF;

    -- T5: com disciplinas, abre
    INSERT INTO disciplina (codigo, nome, semestre) VALUES ('TST0001', 'Disciplina Teste', '9999/1')
    RETURNING id_disciplina INTO v_disc;
    INSERT INTO disciplina (codigo, nome, semestre) VALUES ('TST0002', 'Disciplina Outro Semestre', '9999/2')
    RETURNING id_disciplina INTO v_disc2;
    UPDATE processo_seletivo SET status = 'ABERTO' WHERE id_processo = v_proc;

    -- T6: só um processo ABERTO por vez
    INSERT INTO processo_seletivo (id_usuario, semestre, data_abertura, data_encerramento)
    VALUES (v_adm, '9999/2', CURRENT_DATE, CURRENT_DATE + 30)
    RETURNING id_processo INTO v_proc2;
    v_ok := false;
    BEGIN
        UPDATE processo_seletivo SET status = 'ABERTO' WHERE id_processo = v_proc2;
    EXCEPTION WHEN OTHERS THEN v_ok := true;
    END;
    IF NOT v_ok THEN RAISE EXCEPTION 'TESTE FALHOU: T6 dois processos ABERTOS ao mesmo tempo'; END IF;

    -- T7: matrícula inválida recusada
    v_ok := false;
    BEGIN
        INSERT INTO aluno (matricula, nome, email) VALUES ('123', 'X', 'x@x.com');
    EXCEPTION WHEN OTHERS THEN v_ok := true;
    END;
    IF NOT v_ok THEN RAISE EXCEPTION 'TESTE FALHOU: T7 matrícula inválida aceita'; END IF;

    INSERT INTO aluno (matricula, nome, email)
    VALUES ('999000001', 'Aluno de Teste', 'aluno@teste.local')
    RETURNING id_aluno INTO v_aluno;

    -- T8: coeficiente errado recusado (4.50 e SS => 4.70)
    v_ok := false;
    BEGIN
        INSERT INTO inscricao (id_aluno, id_disciplina, id_processo, ira, mencao, coeficiente, caminho_historico)
        VALUES (v_aluno, v_disc, v_proc, 4.50, 'SS', 4.00, 'h.pdf');
    EXCEPTION WHEN OTHERS THEN v_ok := true;
    END;
    IF NOT v_ok THEN RAISE EXCEPTION 'TESTE FALHOU: T8 coeficiente incorreto aceito'; END IF;

    -- T9: disciplina de outro semestre recusada
    v_ok := false;
    BEGIN
        INSERT INTO inscricao (id_aluno, id_disciplina, id_processo, ira, mencao, coeficiente, caminho_historico)
        VALUES (v_aluno, v_disc2, v_proc, 4.50, 'SS', 4.70, 'h.pdf');
    EXCEPTION WHEN OTHERS THEN v_ok := true;
    END;
    IF NOT v_ok THEN RAISE EXCEPTION 'TESTE FALHOU: T9 disciplina de outro semestre aceita'; END IF;

    -- T10: inscrição em processo não aberto recusada
    v_ok := false;
    BEGIN
        INSERT INTO inscricao (id_aluno, id_disciplina, id_processo, ira, mencao, coeficiente, caminho_historico)
        VALUES (v_aluno, v_disc2, v_proc2, 4.50, 'SS', 4.70, 'h.pdf');
    EXCEPTION WHEN OTHERS THEN v_ok := true;
    END;
    IF NOT v_ok THEN RAISE EXCEPTION 'TESTE FALHOU: T10 inscrição em processo não aberto aceita'; END IF;

    -- T11: inscrição válida; segunda inscrição no mesmo processo recusada
    INSERT INTO inscricao (id_aluno, id_disciplina, id_processo, ira, mencao, coeficiente, caminho_historico)
    VALUES (v_aluno, v_disc, v_proc, 4.50, 'SS', 4.70, 'h.pdf')
    RETURNING id_inscricao INTO v_insc;
    v_ok := false;
    BEGIN
        INSERT INTO inscricao (id_aluno, id_disciplina, id_processo, ira, mencao, coeficiente, caminho_historico)
        VALUES (v_aluno, v_disc, v_proc, 4.50, 'SS', 4.70, 'h.pdf');
    EXCEPTION WHEN OTHERS THEN v_ok := true;
    END;
    IF NOT v_ok THEN RAISE EXCEPTION 'TESTE FALHOU: T11 inscrição duplicada no processo aceita'; END IF;

    -- T12: aparece como pendente e no ranking
    SELECT count(*) INTO n FROM vw_inscricoes_pendentes WHERE id_inscricao = v_insc;
    IF n <> 1 THEN RAISE EXCEPTION 'TESTE FALHOU: T12 inscrição não aparece em vw_inscricoes_pendentes'; END IF;
    SELECT count(*) INTO n FROM vw_ranking_geral WHERE matricula = '999000001';
    IF n <> 1 THEN RAISE EXCEPTION 'TESTE FALHOU: T12 inscrição não aparece em vw_ranking_geral'; END IF;

    -- T13: não encerra com inscrição sem resultado
    v_ok := false;
    BEGIN
        UPDATE processo_seletivo SET status = 'ENCERRADO' WHERE id_processo = v_proc;
    EXCEPTION WHEN OTHERS THEN v_ok := true;
    END;
    IF NOT v_ok THEN RAISE EXCEPTION 'TESTE FALHOU: T13 encerrou com inscrição sem resultado'; END IF;

    -- T14: aprovado sem modalidade recusado; resultado correto aceito
    v_ok := false;
    BEGIN
        INSERT INTO resultado (id_inscricao, decisao) VALUES (v_insc, 'APROVADO');
    EXCEPTION WHEN OTHERS THEN v_ok := true;
    END;
    IF NOT v_ok THEN RAISE EXCEPTION 'TESTE FALHOU: T14 aprovado sem modalidade aceito'; END IF;
    INSERT INTO resultado (id_inscricao, decisao, modalidade)
    VALUES (v_insc, 'APROVADO', 'BOLSISTA') RETURNING id_resultado INTO v_res;

    -- T15: não encerra com e-mail pendente
    v_ok := false;
    BEGIN
        UPDATE processo_seletivo SET status = 'ENCERRADO' WHERE id_processo = v_proc;
    EXCEPTION WHEN OTHERS THEN v_ok := true;
    END;
    IF NOT v_ok THEN RAISE EXCEPTION 'TESTE FALHOU: T15 encerrou com e-mail pendente'; END IF;

    -- T16: marca e-mail enviado; depois o resultado fica travado
    UPDATE resultado SET email_enviado = true, data_envio = now() WHERE id_resultado = v_res;
    v_ok := false;
    BEGIN
        UPDATE resultado SET decisao = 'REPROVADO', modalidade = NULL WHERE id_resultado = v_res;
    EXCEPTION WHEN OTHERS THEN v_ok := true;
    END;
    IF NOT v_ok THEN RAISE EXCEPTION 'TESTE FALHOU: T16 resultado alterado após envio do e-mail'; END IF;

    -- T17: não exclui aluno com inscrição em processo não encerrado
    v_ok := false;
    BEGIN
        DELETE FROM aluno WHERE id_aluno = v_aluno;
    EXCEPTION WHEN OTHERS THEN v_ok := true;
    END;
    IF NOT v_ok THEN RAISE EXCEPTION 'TESTE FALHOU: T17 excluiu aluno com processo em andamento'; END IF;

    -- T18: não exclui nem limpa processo que não está encerrado
    v_ok := false;
    BEGIN
        PERFORM limpar_processo_encerrado(v_proc);
    EXCEPTION WHEN OTHERS THEN v_ok := true;
    END;
    IF NOT v_ok THEN RAISE EXCEPTION 'TESTE FALHOU: T18 limpeza de processo não encerrado'; END IF;

    -- T19: encerra com tudo decidido e enviado
    UPDATE processo_seletivo SET status = 'ENCERRADO' WHERE id_processo = v_proc;

    -- T20: não reabre processo encerrado
    v_ok := false;
    BEGIN
        UPDATE processo_seletivo SET status = 'ABERTO' WHERE id_processo = v_proc;
    EXCEPTION WHEN OTHERS THEN v_ok := true;
    END;
    IF NOT v_ok THEN RAISE EXCEPTION 'TESTE FALHOU: T20 reabriu processo encerrado'; END IF;

    -- T21: limpeza apaga aluno, inscrição, resultado, processo e disciplinas do semestre
    PERFORM limpar_processo_encerrado(v_proc);
    SELECT count(*) INTO n FROM aluno WHERE id_aluno = v_aluno;
    IF n <> 0 THEN RAISE EXCEPTION 'TESTE FALHOU: T21 aluno não foi apagado'; END IF;
    SELECT count(*) INTO n FROM inscricao WHERE id_inscricao = v_insc;
    IF n <> 0 THEN RAISE EXCEPTION 'TESTE FALHOU: T21 inscrição não foi apagada'; END IF;
    SELECT count(*) INTO n FROM resultado WHERE id_resultado = v_res;
    IF n <> 0 THEN RAISE EXCEPTION 'TESTE FALHOU: T21 resultado não foi apagado'; END IF;
    SELECT count(*) INTO n FROM processo_seletivo WHERE id_processo = v_proc;
    IF n <> 0 THEN RAISE EXCEPTION 'TESTE FALHOU: T21 processo não foi apagado'; END IF;
    SELECT count(*) INTO n FROM disciplina WHERE id_disciplina = v_disc;
    IF n <> 0 THEN RAISE EXCEPTION 'TESTE FALHOU: T21 disciplina do semestre não foi apagada'; END IF;
    SELECT count(*) INTO n FROM disciplina WHERE id_disciplina = v_disc2;
    IF n <> 1 THEN RAISE EXCEPTION 'TESTE FALHOU: T21 apagou disciplina de outro semestre'; END IF;

    RAISE NOTICE 'Regras do banco: OK';
END
$$;

-- Permissões do papel da aplicação (exige o 03_setup_usuario.sql já executado)
SET LOCAL ROLE monitora_app;

DO $$
DECLARE
    v_ok boolean := false;
    n    integer;
BEGIN
    SELECT count(*) INTO n FROM public.vw_ranking_geral;
    SELECT count(*) INTO n FROM public.vw_ranking_por_disciplina;
    SELECT count(*) INTO n FROM public.vw_inscricoes_pendentes;
    SELECT count(*) INTO n FROM public.vw_total_inscritos_disciplina;
    SELECT count(*) INTO n FROM public.usuario_administrador;

    -- a aplicação consegue cadastrar aluno...
    INSERT INTO public.aluno (matricula, nome, email)
    VALUES ('999000002', 'Teste Permissao', 'perm@teste.local');

    -- ...mas não consegue apagar alunos diretamente
    BEGIN
        DELETE FROM public.aluno;
    EXCEPTION WHEN insufficient_privilege THEN v_ok := true;
    END;
    IF NOT v_ok THEN RAISE EXCEPTION 'TESTE FALHOU: monitora_app consegue DELETE em aluno'; END IF;

    RAISE NOTICE 'Permissões do monitora_app: OK';
END
$$;

RESET ROLE;
ROLLBACK;

SELECT 'TODOS OS TESTES PASSARAM (nada foi gravado: ROLLBACK)' AS resultado;
