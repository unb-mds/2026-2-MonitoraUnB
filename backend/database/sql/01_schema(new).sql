
CREATE TABLE public.aluno (
    id_aluno  integer GENERATED ALWAYS AS IDENTITY,
    matricula character varying(9)   NOT NULL,
    nome      character varying(150) NOT NULL,
    email     character varying(150) NOT NULL,
    CONSTRAINT aluno_pkey PRIMARY KEY (id_aluno),
    CONSTRAINT aluno_matricula_key UNIQUE (matricula),
    CONSTRAINT chk_matricula CHECK (matricula ~ '^[0-9]{9}$'),
    CONSTRAINT chk_aluno_nome CHECK (btrim(nome) <> ''),
    CONSTRAINT chk_aluno_email CHECK (email ~ '^[^@[:space:]]+@[^@[:space:]]+$')
);

CREATE TABLE public.disciplina (
    id_disciplina integer GENERATED ALWAYS AS IDENTITY,
    codigo        character varying(30)  NOT NULL,
    nome          character varying(150) NOT NULL,
    -- Mesmo formato de processo_seletivo.semestre (ex.: '2026/2').
    -- A mesma disciplina volta a cada semestre, por isso a unicidade é
    -- (codigo, semestre). O scraper faz upsert por essa chave.
    semestre      character varying(20)  NOT NULL,
    CONSTRAINT disciplina_pkey PRIMARY KEY (id_disciplina),
    CONSTRAINT disciplina_codigo_semestre_key UNIQUE (codigo, semestre),
    -- Formato único (AAAA/N) para que processo e disciplinas sempre combinem.
    CONSTRAINT chk_disciplina_semestre CHECK (semestre ~ '^[0-9]{4}/[0-9]$')
);

CREATE TABLE public.usuario_administrador (
    id_usuario integer GENERATED ALWAYS AS IDENTITY,
    email      character varying(150) NOT NULL,
    senha_hash text    NOT NULL,
    ativo      boolean DEFAULT true NOT NULL,
    CONSTRAINT usuario_administrador_pkey PRIMARY KEY (id_usuario),
    CONSTRAINT uq_usuario_admin_email UNIQUE (email)
);

-- CORREÇÃO: id_processo não tinha IDENTITY (a sequence
-- processo_seletivo_id_processo_seq do 03_setup_usuario.sql não existia).
CREATE TABLE public.processo_seletivo (
    id_processo       integer GENERATED ALWAYS AS IDENTITY,
    id_usuario        integer NOT NULL,
    semestre          character varying(20) NOT NULL,
    data_abertura     date NOT NULL,
    data_encerramento date NOT NULL,
    status            character varying(20) DEFAULT 'AGENDADO' NOT NULL,
    CONSTRAINT processo_seletivo_pkey PRIMARY KEY (id_processo),
    CONSTRAINT fk_processo_usuario
        FOREIGN KEY (id_usuario) REFERENCES public.usuario_administrador(id_usuario),
    CONSTRAINT chk_datas_processo CHECK (data_encerramento >= data_abertura),
    CONSTRAINT chk_processo_semestre CHECK (semestre ~ '^[0-9]{4}/[0-9]$'),
    CONSTRAINT chk_status_processo
        CHECK (status IN ('AGENDADO', 'ABERTO', 'ENCERRADO'))
);

CREATE TABLE public.inscricao (
    id_inscricao      integer GENERATED ALWAYS AS IDENTITY,
    id_aluno          integer NOT NULL,
    id_disciplina     integer NOT NULL,
    id_processo       integer NOT NULL,
    ira               numeric(4,2) NOT NULL,
    mencao            character varying(10) NOT NULL,
    coeficiente       numeric(4,2) NOT NULL,
    caminho_historico text NOT NULL,
    data_inscricao    timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT inscricao_pkey PRIMARY KEY (id_inscricao),
    -- Atenção: um aluno só pode ter UMA inscrição por processo (em uma só disciplina).
    CONSTRAINT uq_aluno_processo UNIQUE (id_aluno, id_processo),
    CONSTRAINT fk_inscricao_aluno
        FOREIGN KEY (id_aluno) REFERENCES public.aluno(id_aluno) ON DELETE CASCADE,
    CONSTRAINT fk_inscricao_disciplina
        FOREIGN KEY (id_disciplina) REFERENCES public.disciplina(id_disciplina),
    CONSTRAINT fk_inscricao_processo
        FOREIGN KEY (id_processo) REFERENCES public.processo_seletivo(id_processo)
        ON DELETE CASCADE,
    CONSTRAINT chk_ira_limite CHECK (ira >= 0 AND ira <= 5),
    CONSTRAINT chk_mencao CHECK (mencao IN ('MM', 'MS', 'SS')),
    CONSTRAINT chk_coeficiente_calculo CHECK (
        coeficiente = round((0.6 * ira) + (0.4 * (
            CASE mencao
                WHEN 'MM' THEN 3
                WHEN 'MS' THEN 4
                WHEN 'SS' THEN 5
            END)::numeric), 2)
    )
);

CREATE TABLE public.resultado (
    id_resultado  integer GENERATED ALWAYS AS IDENTITY,
    id_inscricao  integer NOT NULL,
    decisao       character varying(20) NOT NULL,
    modalidade    character varying(20),
    data_decisao  timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    email_enviado boolean DEFAULT false NOT NULL,
    data_envio    timestamp without time zone,
    CONSTRAINT resultado_pkey PRIMARY KEY (id_resultado),
    CONSTRAINT resultado_id_inscricao_key UNIQUE (id_inscricao),
    CONSTRAINT fk_resultado_inscricao
        FOREIGN KEY (id_inscricao) REFERENCES public.inscricao(id_inscricao)
        ON DELETE CASCADE,
    CONSTRAINT chk_decisao CHECK (decisao IN ('APROVADO', 'REPROVADO')),
    CONSTRAINT chk_envio_email CHECK (
        (email_enviado = false AND data_envio IS NULL)
        OR (email_enviado = true AND data_envio IS NOT NULL)
    ),
    CONSTRAINT chk_modalidade CHECK (
        -- IS NOT NULL é necessário: sem ele, modalidade NULL daria NULL
        -- (e o CHECK aceita NULL), permitindo APROVADO sem modalidade.
        (decisao = 'APROVADO' AND modalidade IS NOT NULL
            AND modalidade IN ('BOLSISTA', 'VOLUNTARIO'))
        OR (decisao = 'REPROVADO' AND modalidade IS NULL)
    )
);

-- ---------------------------------------------------------------------
-- Índices
-- ---------------------------------------------------------------------

-- Garante no máximo um processo ABERTO por vez
CREATE UNIQUE INDEX uq_processo_aberto
    ON public.processo_seletivo USING btree (status)
    WHERE status = 'ABERTO';

-- CORREÇÃO: FKs sem índice (o Postgres não cria automaticamente).
-- Aceleram as views, os triggers e os DELETE ... CASCADE.
CREATE INDEX idx_inscricao_processo   ON public.inscricao (id_processo);
CREATE INDEX idx_inscricao_disciplina ON public.inscricao (id_disciplina);
CREATE INDEX idx_processo_usuario     ON public.processo_seletivo (id_usuario);

-- ---------------------------------------------------------------------
-- Funções e triggers
-- ---------------------------------------------------------------------

CREATE FUNCTION public.bloquear_alteracao_resultado_enviado() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    IF OLD.email_enviado = TRUE THEN
        RAISE EXCEPTION
            'Este resultado não pode ser alterado: o e-mail já foi enviado.';
    END IF;

    -- CORREÇÃO: impede "trocar" o resultado de uma inscrição para outra.
    IF NEW.id_inscricao IS DISTINCT FROM OLD.id_inscricao THEN
        RAISE EXCEPTION
            'Não é permitido alterar a inscrição vinculada ao resultado.';
    END IF;

    IF NEW.email_enviado = TRUE
       AND (
           NEW.decisao IS DISTINCT FROM OLD.decisao
           OR NEW.modalidade IS DISTINCT FROM OLD.modalidade
       ) THEN
        RAISE EXCEPTION
            'A decisão deve ser registrada antes do envio do e-mail.';
    END IF;

    RETURN NEW;
END;
$$;

-- CORREÇÃO: agora valida TODAS as transições de status e a criação
-- (antes só validava o encerramento; era possível reabrir um processo
-- ENCERRADO ou voltar ABERTO -> AGENDADO).
-- Transições permitidas: AGENDADO -> ABERTO -> ENCERRADO.
CREATE FUNCTION public.validar_transicao_processo() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    -- Todo processo nasce AGENDADO.
    IF TG_OP = 'INSERT' THEN
        IF NEW.status <> 'AGENDADO' THEN
            RAISE EXCEPTION
                'Todo processo seletivo deve ser criado com status AGENDADO.';
        END IF;
        RETURN NEW;
    END IF;

    IF NEW.status IS NOT DISTINCT FROM OLD.status THEN
        RETURN NEW;
    END IF;

    IF NOT (
        (OLD.status = 'AGENDADO' AND NEW.status = 'ABERTO')
        OR (OLD.status = 'ABERTO' AND NEW.status = 'ENCERRADO')
    ) THEN
        RAISE EXCEPTION
            'Transição de status inválida: % -> %.', OLD.status, NEW.status;
    END IF;

    -- Abrir sem disciplinas do semestre (scraper ainda não rodou) deixaria
    -- o processo aberto mas sem ninguém conseguir se inscrever.
    IF NEW.status = 'ABERTO' THEN
        IF NOT EXISTS (
            SELECT 1 FROM disciplina d WHERE d.semestre = NEW.semestre
        ) THEN
            RAISE EXCEPTION
                'Não é possível abrir: não há disciplinas cadastradas para o semestre %.',
                NEW.semestre;
        END IF;
    END IF;

    IF NEW.status = 'ENCERRADO' THEN
        IF EXISTS (
            SELECT 1
            FROM inscricao i
            LEFT JOIN resultado r
                ON r.id_inscricao = i.id_inscricao
            WHERE i.id_processo = NEW.id_processo
              AND (
                  r.id_resultado IS NULL
                  OR r.email_enviado IS DISTINCT FROM TRUE
              )
        ) THEN
            RAISE EXCEPTION
                'Não é possível encerrar: existem inscrições sem decisão ou e-mails pendentes.';
        END IF;
    END IF;

    RETURN NEW;
END;
$$;

CREATE FUNCTION public.validar_exclusao_aluno() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM inscricao i
        JOIN processo_seletivo p
            ON p.id_processo = i.id_processo
        WHERE i.id_aluno = OLD.id_aluno
          AND p.status <> 'ENCERRADO'
    ) THEN
        RAISE EXCEPTION
            'Não é possível excluir o aluno enquanto houver inscrição vinculada a um processo não encerrado.';
    END IF;

    RETURN OLD;
END;
$$;

CREATE FUNCTION public.validar_exclusao_processo() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    IF OLD.status <> 'ENCERRADO' THEN
        RAISE EXCEPTION
            'Não é possível excluir um processo que não foi encerrado.';
    END IF;

    RETURN OLD;
END;
$$;

CREATE FUNCTION public.validar_inscricao_processo() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
    situacao_processo VARCHAR(20);
    semestre_processo VARCHAR(20);
BEGIN
    SELECT status, semestre
    INTO situacao_processo, semestre_processo
    FROM processo_seletivo
    WHERE id_processo = NEW.id_processo
    FOR SHARE;

    IF situacao_processo IS DISTINCT FROM 'ABERTO' THEN
        RAISE EXCEPTION
            'Não é possível realizar a inscrição: o processo seletivo não está aberto.';
    END IF;

    -- A disciplina precisa ser do mesmo semestre do processo.
    IF NOT EXISTS (
        SELECT 1
        FROM disciplina d
        WHERE d.id_disciplina = NEW.id_disciplina
          AND d.semestre = semestre_processo
    ) THEN
        RAISE EXCEPTION
            'A disciplina não pertence ao semestre do processo seletivo.';
    END IF;

    RETURN NEW;
END;
$$;

-- CORREÇÃO: SECURITY DEFINER + search_path fixo.
-- O papel da aplicação não tem DELETE em aluno/processo_seletivo, então
-- sem isso a função falharia para ele. A função já valida todas as
-- condições antes de apagar. O EXECUTE é liberado no 03_setup_usuario.sql.
CREATE FUNCTION public.limpar_processo_encerrado(p_id_processo integer) RETURNS void
    LANGUAGE plpgsql
    SECURITY DEFINER
    SET search_path = public, pg_temp
    AS $$
DECLARE
    v_status   VARCHAR(20);
    v_semestre VARCHAR(20);
BEGIN
    SELECT status, semestre
    INTO v_status, v_semestre
    FROM processo_seletivo
    WHERE id_processo = p_id_processo
    FOR UPDATE;

    IF NOT FOUND THEN
        RAISE EXCEPTION
            'Processo seletivo não encontrado.';
    END IF;

    IF v_status <> 'ENCERRADO' THEN
        RAISE EXCEPTION
            'A limpeza só pode ser realizada em processos encerrados.';
    END IF;

    IF EXISTS (
        SELECT 1
        FROM inscricao i
        LEFT JOIN resultado r
            ON r.id_inscricao = i.id_inscricao
        WHERE i.id_processo = p_id_processo
          AND (
              r.id_resultado IS NULL
              OR r.email_enviado IS DISTINCT FROM TRUE
          )
    ) THEN
        RAISE EXCEPTION
            'Existem resultados ou e-mails pendentes.';
    END IF;

    IF EXISTS (
        SELECT 1
        FROM inscricao i
        JOIN inscricao outra
            ON outra.id_aluno = i.id_aluno
        WHERE i.id_processo = p_id_processo
          AND outra.id_processo <> p_id_processo
    ) THEN
        RAISE EXCEPTION
            'Existem alunos vinculados a outros processos. Limpeza cancelada.';
    END IF;

    DELETE FROM aluno a
    WHERE EXISTS (
        SELECT 1
        FROM inscricao i
        WHERE i.id_aluno = a.id_aluno
          AND i.id_processo = p_id_processo
    );

    DELETE FROM processo_seletivo
    WHERE id_processo = p_id_processo;

    -- As disciplinas do semestre do processo (carregadas pelo scraper) também
    -- são limpas. Disciplinas de outros semestres, como as do próximo
    -- semestre já carregadas, não são tocadas. O NOT EXISTS protege a FK
    -- caso outro processo do mesmo semestre ainda use a disciplina.
    DELETE FROM disciplina d
    WHERE d.semestre = v_semestre
      AND NOT EXISTS (
          SELECT 1
          FROM inscricao i
          WHERE i.id_disciplina = d.id_disciplina
      );
END;
$$;

CREATE TRIGGER trg_bloquear_resultado_enviado
BEFORE UPDATE ON public.resultado
FOR EACH ROW
EXECUTE FUNCTION public.bloquear_alteracao_resultado_enviado();

CREATE TRIGGER trg_validar_transicao_processo
BEFORE INSERT OR UPDATE OF status ON public.processo_seletivo
FOR EACH ROW
EXECUTE FUNCTION public.validar_transicao_processo();

CREATE TRIGGER trg_validar_exclusao_aluno
BEFORE DELETE ON public.aluno
FOR EACH ROW
EXECUTE FUNCTION public.validar_exclusao_aluno();

CREATE TRIGGER trg_validar_exclusao_processo
BEFORE DELETE ON public.processo_seletivo
FOR EACH ROW
EXECUTE FUNCTION public.validar_exclusao_processo();

CREATE TRIGGER trg_validar_inscricao_processo
BEFORE INSERT OR UPDATE OF id_processo, id_disciplina ON public.inscricao
FOR EACH ROW
EXECUTE FUNCTION public.validar_inscricao_processo();

-- ---------------------------------------------------------------------
-- Views
-- ---------------------------------------------------------------------

-- CORREÇÃO: inclui id_inscricao, necessário para o app registrar o
-- resultado (INSERT em resultado) de uma inscrição pendente.
CREATE VIEW public.vw_inscricoes_pendentes AS
 SELECT i.id_inscricao,
    a.nome,
    a.matricula,
    a.email,
    d.codigo AS codigo_disciplina,
    i.ira,
    i.mencao,
    i.coeficiente,
    i.caminho_historico
   FROM public.inscricao i
     JOIN public.aluno a ON a.id_aluno = i.id_aluno
     JOIN public.disciplina d ON d.id_disciplina = i.id_disciplina
     JOIN public.processo_seletivo p ON p.id_processo = i.id_processo
     LEFT JOIN public.resultado r ON r.id_inscricao = i.id_inscricao
  WHERE p.status = 'ABERTO' AND r.id_resultado IS NULL;

CREATE VIEW public.vw_ranking_geral AS
 SELECT dense_rank() OVER (ORDER BY i.coeficiente DESC) AS posicao,
    a.nome,
    a.matricula,
    a.email,
    d.codigo AS codigo_disciplina,
    d.nome AS disciplina,
    i.ira,
    i.mencao,
    i.coeficiente
   FROM public.inscricao i
     JOIN public.aluno a ON a.id_aluno = i.id_aluno
     JOIN public.disciplina d ON d.id_disciplina = i.id_disciplina
     JOIN public.processo_seletivo p ON p.id_processo = i.id_processo
  WHERE p.status = 'ABERTO';

CREATE VIEW public.vw_ranking_por_disciplina AS
 SELECT dense_rank() OVER (PARTITION BY i.id_disciplina ORDER BY i.coeficiente DESC) AS posicao,
    a.nome,
    a.matricula,
    a.email,
    d.codigo AS codigo_disciplina,
    d.nome AS disciplina,
    i.ira,
    i.mencao,
    i.coeficiente
   FROM public.inscricao i
     JOIN public.aluno a ON a.id_aluno = i.id_aluno
     JOIN public.disciplina d ON d.id_disciplina = i.id_disciplina
     JOIN public.processo_seletivo p ON p.id_processo = i.id_processo
  WHERE p.status = 'ABERTO';

CREATE VIEW public.vw_total_inscritos_disciplina AS
 SELECT d.codigo,
    d.nome AS disciplina,
    count(i.id_inscricao) FILTER (WHERE p.status = 'ABERTO') AS total_inscritos
   FROM public.disciplina d
     LEFT JOIN public.inscricao i ON i.id_disciplina = d.id_disciplina
     LEFT JOIN public.processo_seletivo p ON p.id_processo = i.id_processo
  GROUP BY d.id_disciplina, d.codigo, d.nome;
