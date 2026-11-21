CREATE TABLE public.aluno (
    id_aluno integer NOT NULL,
    matricula character varying(9) NOT NULL,
    nome character varying(150) NOT NULL,
    email character varying(150) NOT NULL,
    CONSTRAINT chk_matricula CHECK (((matricula)::text ~ '^[0-9]{9}$'::text))
);

ALTER TABLE ONLY public.aluno
    ADD CONSTRAINT aluno_matricula_key UNIQUE (matricula);

ALTER TABLE ONLY public.aluno
    ADD CONSTRAINT aluno_pkey PRIMARY KEY (id_aluno);


ALTER TABLE public.aluno ALTER COLUMN id_aluno ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.aluno_id_aluno_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);

CREATE TABLE public.departamentos (
    id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    sigaa_id integer NOT NULL UNIQUE,
    nome character varying(300) NOT NULL,
    created_at timestamp DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE public.disciplina (
    id_disciplina integer NOT NULL,
    codigo character varying(30) NOT NULL,
    nome character varying(300) NOT NULL,
    tipo character varying(50),
    nivel character varying(50),
    carga_horaria integer,
    departamento_id integer,
    created_at timestamp DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE ONLY public.disciplina
    ADD CONSTRAINT disciplina_codigo_key UNIQUE (codigo);

ALTER TABLE ONLY public.disciplina
    ADD CONSTRAINT disciplina_pkey PRIMARY KEY (id_disciplina);

ALTER TABLE ONLY public.disciplina
    ADD CONSTRAINT fk_disciplina_departamento
    FOREIGN KEY (departamento_id)
    REFERENCES public.departamentos(id);

ALTER TABLE public.disciplina ALTER COLUMN id_disciplina ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.disciplina_id_disciplina_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


CREATE TABLE public.processo_seletivo (
    id_processo integer GENERATED ALWAYS AS IDENTITY,
    id_usuario integer NOT NULL,
    semestre character varying(20) NOT NULL,
    data_abertura date NOT NULL,
    data_encerramento date NOT NULL,
    status character varying(20) DEFAULT 'AGENDADO'::character varying NOT NULL,
    CONSTRAINT chk_datas_processo CHECK ((data_encerramento >= data_abertura)),
    CONSTRAINT chk_status_processo CHECK (((status)::text = ANY ((ARRAY['AGENDADO'::character varying, 'ABERTO'::character varying, 'ENCERRADO'::character varying])::text[])))
);

ALTER TABLE ONLY public.processo_seletivo
    ADD CONSTRAINT processo_seletivo_pkey PRIMARY KEY (id_processo);


CREATE TABLE public.usuario_administrador (
    id_usuario integer NOT NULL,
    email character varying(150) NOT NULL,
    senha_hash text NOT NULL,
    ativo boolean DEFAULT true NOT NULL
);

ALTER TABLE ONLY public.usuario_administrador
    ADD CONSTRAINT uq_usuario_admin_email UNIQUE (email);

ALTER TABLE ONLY public.usuario_administrador
    ADD CONSTRAINT usuario_administrador_pkey PRIMARY KEY (id_usuario);


ALTER TABLE ONLY public.processo_seletivo
    ADD CONSTRAINT fk_processo_usuario
    FOREIGN KEY (id_usuario)
    REFERENCES public.usuario_administrador(id_usuario);


ALTER TABLE public.usuario_administrador ALTER COLUMN id_usuario ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.usuario_administrador_id_usuario_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


CREATE UNIQUE INDEX uq_processo_aberto
ON public.processo_seletivo USING btree (status)
WHERE ((status)::text = 'ABERTO'::text);
