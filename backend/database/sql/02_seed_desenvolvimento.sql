-- =====================================================================
-- 02_seed.sql — SOMENTE PARA DESENVOLVIMENTO/TESTE. Nunca rodar em produção.
-- Em produção: o processo é criado por um administrador pelo app e as
-- disciplinas são carregadas pelo scraper do SIGAA.
-- Rodar com o dono do banco, DEPOIS do 01_schema.sql.
-- =====================================================================

CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- 1) Administrador de teste (senha: 'trocar-esta-senha').
--    Hash bcrypt gerado pelo pgcrypto. Se o backend usar outro algoritmo,
--    gere o hash com a biblioteca do backend e cole aqui.
INSERT INTO public.usuario_administrador (email, senha_hash)
VALUES ('professor@teste.local', crypt('trocar-esta-senha', gen_salt('bf', 10)))
ON CONFLICT (email) DO NOTHING;

-- 2) Processo do semestre, criado como AGENDADO (único status permitido na criação).
INSERT INTO public.processo_seletivo
    (id_usuario, semestre, data_abertura, data_encerramento)
SELECT u.id_usuario, '2026/2', DATE '2026-11-01', DATE '2026-12-15'
FROM public.usuario_administrador u
WHERE u.email = 'professor@teste.local'
  AND NOT EXISTS (
      SELECT 1 FROM public.processo_seletivo WHERE semestre = '2026/2'
  );

-- 3) Disciplinas do mesmo semestre (formato AAAA/N, igual ao do processo).
--    Troque pelos códigos que o front/API realmente envia.
INSERT INTO public.disciplina (codigo, nome, semestre) VALUES
    ('CIC0004', 'Algoritmos e Programação de Computadores', '2026/2'),
    ('CIC0097', 'Bancos de Dados',                          '2026/2')
ON CONFLICT (codigo, semestre) DO NOTHING;

-- 4) Abre o processo (o banco exige disciplinas cadastradas para abrir).
UPDATE public.processo_seletivo
SET status = 'ABERTO'
WHERE semestre = '2026/2' AND status = 'AGENDADO';

-- 5) (Opcional) Alunos e inscrições de exemplo, para testar rankings e a
--    tela do professor. Coeficiente = round(0,6 × IRA + 0,4 × nota da menção),
--    com MM = 3, MS = 4, SS = 5; o banco rejeita valores que não batam.
INSERT INTO public.aluno (matricula, nome, email) VALUES
    ('200000001', 'Aluno Teste Um',   'aluno1@teste.local'),
    ('200000002', 'Aluno Teste Dois', 'aluno2@teste.local'),
    ('200000003', 'Aluno Teste Três', 'aluno3@teste.local')
ON CONFLICT (matricula) DO NOTHING;

INSERT INTO public.inscricao
    (id_aluno, id_disciplina, id_processo, ira, mencao, coeficiente, caminho_historico)
SELECT a.id_aluno, d.id_disciplina, p.id_processo,
       v.ira, v.mencao, v.coeficiente, v.caminho
FROM (VALUES
    ('200000001', 'CIC0097', 4.50, 'SS', 4.70, 'historicos/200000001.pdf'),
    ('200000002', 'CIC0097', 3.80, 'MS', 3.88, 'historicos/200000002.pdf'),
    ('200000003', 'CIC0004', 4.00, 'MM', 3.60, 'historicos/200000003.pdf')
) AS v(matricula, codigo, ira, mencao, coeficiente, caminho)
JOIN public.aluno a             ON a.matricula = v.matricula
JOIN public.processo_seletivo p ON p.semestre = '2026/2'
JOIN public.disciplina d        ON d.codigo = v.codigo AND d.semestre = p.semestre
ON CONFLICT (id_aluno, id_processo) DO NOTHING;
