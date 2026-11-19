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

CREATE TABLE public.disciplina (
    id_disciplina integer NOT NULL,
    codigo character varying(30) NOT NULL,
    nome character varying(150) NOT NULL
);

ALTER TABLE ONLY public.disciplina
    ADD CONSTRAINT disciplina_codigo_key UNIQUE (codigo);

ALTER TABLE ONLY public.disciplina
    ADD CONSTRAINT disciplina_pkey PRIMARY KEY (id_disciplina);

ALTER TABLE public.disciplina ALTER COLUMN id_disciplina ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.disciplina_id_disciplina_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);

CREATE TABLE public.inscricao (
    id_inscricao integer NOT NULL,
    id_aluno integer NOT NULL,
    id_disciplina integer NOT NULL,
    id_processo integer NOT NULL,
    ira numeric(4,2) NOT NULL,
    mencao character varying(10) NOT NULL,
    coeficiente numeric(4,2) NOT NULL,
    caminho_historico text NOT NULL,
    data_inscricao timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT chk_coeficiente_calculo CHECK ((coeficiente = round(((0.6 * ira) + (0.4 * (
CASE mencao
    WHEN 'MM'::text THEN 3
    WHEN 'MS'::text THEN 4
    WHEN 'SS'::text THEN 5
    ELSE NULL::integer
END)::numeric)), 2))),
    CONSTRAINT chk_ira_limite CHECK (((ira >= (0)::numeric) AND (ira <= (5)::numeric))),
    CONSTRAINT chk_mencao CHECK (((mencao)::text = ANY ((ARRAY['MM'::character varying, 'MS'::character varying, 'SS'::character varying])::text[])))
);


ALTER TABLE ONLY public.inscricao
    ADD CONSTRAINT inscricao_pkey PRIMARY KEY (id_inscricao);

ALTER TABLE ONLY public.inscricao
    ADD CONSTRAINT uq_aluno_processo UNIQUE (id_aluno, id_processo);

ALTER TABLE ONLY public.inscricao
    ADD CONSTRAINT fk_inscricao_aluno
    FOREIGN KEY (id_aluno)
    REFERENCES public.aluno(id_aluno)
    ON DELETE CASCADE;

ALTER TABLE ONLY public.inscricao
    ADD CONSTRAINT fk_inscricao_disciplina
    FOREIGN KEY (id_disciplina)
    REFERENCES public.disciplina(id_disciplina);

ALTER TABLE public.inscricao ALTER COLUMN id_inscricao ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.inscricao_id_inscricao_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);

CREATE TABLE public.processo_seletivo (
    id_processo integer NOT NULL,
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

ALTER TABLE ONLY public.inscricao
    ADD CONSTRAINT fk_inscricao_processo
    FOREIGN KEY (id_processo)
    REFERENCES public.processo_seletivo(id_processo)
    ON DELETE CASCADE;


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

CREATE TABLE public.resultado (
    id_resultado integer NOT NULL,
    id_inscricao integer NOT NULL,
    decisao character varying(20) NOT NULL,
    modalidade character varying(20),
    data_decisao timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    email_enviado boolean DEFAULT false NOT NULL,
    data_envio timestamp without time zone,
    CONSTRAINT chk_decisao CHECK (((decisao)::text = ANY ((ARRAY['APROVADO'::character varying, 'REPROVADO'::character varying])::text[]))),
    CONSTRAINT chk_envio_email CHECK ((((email_enviado = false) AND (data_envio IS NULL)) OR ((email_enviado = true) AND (data_envio IS NOT NULL)))),
    CONSTRAINT chk_modalidade CHECK (((((decisao)::text = 'APROVADO'::text) AND (modalidade IS NOT NULL) AND ((modalidade)::text = ANY ((ARRAY['BOLSISTA'::character varying, 'VOLUNTARIO'::character varying])::text[]))) OR (((decisao)::text = 'REPROVADO'::text) AND (modalidade IS NULL))))
);

ALTER TABLE ONLY public.resultado
    ADD CONSTRAINT resultado_id_inscricao_key UNIQUE (id_inscricao);

ALTER TABLE ONLY public.resultado
    ADD CONSTRAINT resultado_pkey PRIMARY KEY (id_resultado);

ALTER TABLE ONLY public.resultado
    ADD CONSTRAINT fk_resultado_inscricao
    FOREIGN KEY (id_inscricao)
    REFERENCES public.inscricao(id_inscricao)
    ON DELETE CASCADE;

ALTER TABLE public.resultado ALTER COLUMN id_resultado ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.resultado_id_resultado_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


CREATE UNIQUE INDEX uq_processo_aberto
ON public.processo_seletivo USING btree (status)
WHERE ((status)::text = 'ABERTO'::text);

CREATE FUNCTION public.bloquear_alteracao_resultado_enviado() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    IF OLD.email_enviado = TRUE THEN
        RAISE EXCEPTION
            'Este resultado não pode ser alterado: o e-mail já foi enviado.';
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

CREATE FUNCTION public.limpar_processo_encerrado(p_id_processo integer) RETURNS void
    LANGUAGE plpgsql
    AS $$
DECLARE
    v_status VARCHAR(20);
BEGIN
    SELECT status
    INTO v_status
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

END;
$$;


CREATE FUNCTION public.validar_encerramento_processo() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    IF NEW.status = 'ENCERRADO'
       AND OLD.status <> 'ENCERRADO' THEN

        IF OLD.status <> 'ABERTO' THEN
            RAISE EXCEPTION
                'Somente um processo aberto pode ser encerrado.';
        END IF;

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
BEGIN
    SELECT status
    INTO situacao_processo
    FROM processo_seletivo
    WHERE id_processo = NEW.id_processo
    FOR SHARE;

    IF situacao_processo IS DISTINCT FROM 'ABERTO' THEN
        RAISE EXCEPTION
            'Não é possível realizar a inscrição: o processo seletivo não está aberto.';
    END IF;

    RETURN NEW;
END;
$$;


CREATE TRIGGER trg_bloquear_resultado_enviado
BEFORE UPDATE ON public.resultado
FOR EACH ROW
EXECUTE FUNCTION public.bloquear_alteracao_resultado_enviado();


CREATE TRIGGER trg_validar_encerramento_processo
BEFORE UPDATE OF status ON public.processo_seletivo
FOR EACH ROW
EXECUTE FUNCTION public.validar_encerramento_processo();


CREATE TRIGGER trg_validar_exclusao_aluno
BEFORE DELETE ON public.aluno
FOR EACH ROW
EXECUTE FUNCTION public.validar_exclusao_aluno();


CREATE TRIGGER trg_validar_exclusao_processo
BEFORE DELETE ON public.processo_seletivo
FOR EACH ROW
EXECUTE FUNCTION public.validar_exclusao_processo();


CREATE TRIGGER trg_validar_inscricao_processo
BEFORE INSERT OR UPDATE OF id_processo ON public.inscricao
FOR EACH ROW
EXECUTE FUNCTION public.validar_inscricao_processo();


CREATE VIEW public.vw_inscricoes_pendentes AS
 SELECT a.nome,
    a.matricula,
    a.email,
    d.codigo AS codigo_disciplina,
    i.ira,
    i.mencao,
    i.coeficiente,
    i.caminho_historico
   FROM ((((public.inscricao i
     JOIN public.aluno a ON ((a.id_aluno = i.id_aluno)))
     JOIN public.disciplina d ON ((d.id_disciplina = i.id_disciplina)))
     JOIN public.processo_seletivo p ON ((p.id_processo = i.id_processo)))
     LEFT JOIN public.resultado r ON ((r.id_inscricao = i.id_inscricao)))
  WHERE (((p.status)::text = 'ABERTO'::text) AND (r.id_resultado IS NULL));


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
   FROM (((public.inscricao i
     JOIN public.aluno a ON ((a.id_aluno = i.id_aluno)))
     JOIN public.disciplina d ON ((d.id_disciplina = i.id_disciplina)))
     JOIN public.processo_seletivo p ON ((p.id_processo = i.id_processo)))
  WHERE ((p.status)::text = 'ABERTO'::text);


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
   FROM (((public.inscricao i
     JOIN public.aluno a ON ((a.id_aluno = i.id_aluno)))
     JOIN public.disciplina d ON ((d.id_disciplina = i.id_disciplina)))
     JOIN public.processo_seletivo p ON ((p.id_processo = i.id_processo)))
  WHERE ((p.status)::text = 'ABERTO'::text);


CREATE VIEW public.vw_total_inscritos_disciplina AS
 SELECT d.codigo,
    d.nome AS disciplina,
    count(i.id_inscricao) FILTER (WHERE ((p.status)::text = 'ABERTO'::text)) AS total_inscritos
   FROM ((public.disciplina d
     LEFT JOIN public.inscricao i ON ((i.id_disciplina = d.id_disciplina)))
     LEFT JOIN public.processo_seletivo p ON ((p.id_processo = i.id_processo)))
  GROUP BY d.id_disciplina, d.codigo, d.nome;



