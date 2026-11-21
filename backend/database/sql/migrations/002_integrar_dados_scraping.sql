BEGIN;

-- Garante as estruturas-base que o scraper usa em instalações antigas.
CREATE TABLE IF NOT EXISTS public.departamentos (
    id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    sigaa_id integer NOT NULL UNIQUE,
    nome character varying(300) NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE public.disciplina
    ADD COLUMN IF NOT EXISTS tipo character varying(50),
    ADD COLUMN IF NOT EXISTS nivel character varying(50),
    ADD COLUMN IF NOT EXISTS carga_horaria integer,
    ADD COLUMN IF NOT EXISTS departamento_id integer,
    ADD COLUMN IF NOT EXISTS created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    ADD COLUMN IF NOT EXISTS updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    ADD COLUMN IF NOT EXISTS pre_requisitos text,
    ADD COLUMN IF NOT EXISTS co_requisitos text,
    ADD COLUMN IF NOT EXISTS equivalencias text,
    ADD COLUMN IF NOT EXISTS ementa text;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM pg_constraint
        WHERE conrelid = 'public.disciplina'::regclass
          AND confrelid = 'public.departamentos'::regclass
          AND contype = 'f'
    ) THEN
        ALTER TABLE public.disciplina
            ADD CONSTRAINT fk_disciplina_departamento
            FOREIGN KEY (departamento_id)
            REFERENCES public.departamentos(id);
    END IF;
END
$$;

CREATE INDEX IF NOT EXISTS idx_disciplina_nome
    ON public.disciplina USING btree (nome);

CREATE TABLE IF NOT EXISTS public.professores (
    id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome character varying(300) NOT NULL,
    departamento_id integer,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_professor_nome UNIQUE (nome),
    CONSTRAINT fk_professor_departamento
        FOREIGN KEY (departamento_id)
        REFERENCES public.departamentos(id)
);

CREATE TABLE IF NOT EXISTS public.turmas (
    id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    codigo character varying(20) NOT NULL,
    ano_periodo character varying(20) NOT NULL,
    horario character varying(500),
    local character varying(300),
    vagas_ofertadas integer,
    vagas_ocupadas integer,
    disciplina_id integer NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_turma_periodo UNIQUE (disciplina_id, codigo, ano_periodo),
    CONSTRAINT fk_turma_disciplina
        FOREIGN KEY (disciplina_id)
        REFERENCES public.disciplina(id_disciplina)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS public.disciplina_professores (
    disciplina_id integer NOT NULL,
    professor_id integer NOT NULL,
    PRIMARY KEY (disciplina_id, professor_id),
    CONSTRAINT fk_disciplina_professores_disciplina
        FOREIGN KEY (disciplina_id)
        REFERENCES public.disciplina(id_disciplina)
        ON DELETE CASCADE,
    CONSTRAINT fk_disciplina_professores_professor
        FOREIGN KEY (professor_id)
        REFERENCES public.professores(id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS public.turma_professores (
    turma_id integer NOT NULL,
    professor_id integer NOT NULL,
    PRIMARY KEY (turma_id, professor_id),
    CONSTRAINT fk_turma_professores_turma
        FOREIGN KEY (turma_id)
        REFERENCES public.turmas(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_turma_professores_professor
        FOREIGN KEY (professor_id)
        REFERENCES public.professores(id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS public.scraping_logs (
    id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    departamento_sigaa_id integer,
    nivel character varying(50),
    status character varying(20) NOT NULL,
    disciplinas_encontradas integer DEFAULT 0,
    disciplinas_novas integer DEFAULT 0,
    disciplinas_atualizadas integer DEFAULT 0,
    professores_encontrados integer DEFAULT 0,
    turmas_encontradas integer DEFAULT 0,
    mensagem text,
    started_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    finished_at timestamp without time zone
);

ALTER TABLE public.scraping_logs
    ADD COLUMN IF NOT EXISTS professores_encontrados integer DEFAULT 0,
    ADD COLUMN IF NOT EXISTS turmas_encontradas integer DEFAULT 0;

COMMIT;
