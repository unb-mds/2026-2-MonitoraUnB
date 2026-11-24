-- =====================================================================
-- 04_primeiro_admin.sql — cria o PRIMEIRO administrador (uma única vez,
-- na implantação). Nenhuma tela do app cria administradores.
--
-- COMO USAR NO pgAdmin:
--   1) Troque 'admin@dominio.br' e 'SENHA-FORTE' abaixo pelos valores reais.
--   2) Execute. Depois APAGUE a senha do texto da consulta e não salve este
--      arquivo com a senha dentro.
--
-- ATENÇÃO: o hash gerado é bcrypt. Confirme com quem fez o backend que o
-- login valida bcrypt; se usar outro algoritmo (argon2, scrypt...), gere o
-- hash pela biblioteca do backend e insira-o diretamente em senha_hash.
-- =====================================================================

CREATE EXTENSION IF NOT EXISTS pgcrypto;

INSERT INTO public.usuario_administrador (email, senha_hash)
VALUES ('admin@dominio.br', crypt('SENHA-FORTE', gen_salt('bf', 12)));

-- Confere (não mostra a senha, só o e-mail e se está ativo):
SELECT id_usuario, email, ativo FROM public.usuario_administrador;
