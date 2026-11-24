# Banco de dados — Monitora UnB (PostgreSQL, guia de implantação com pgAdmin)

Em cada etapa: abra uma **Query Tool** no banco certo, cole o conteúdo do script
inteiro (sem selecionar trecho) e execute (F5). Use sempre o **dono do banco**
(ex.: `postgres`), nunca `monitora_app`.

## Ordem dos scripts

| Script | Quando | O que faz |
|---|---|---|
| `01_schema.sql` | sempre, 1ª vez, em banco VAZIO | tabelas, regras, triggers, views |
| `03_setup_usuario.sql` | sempre, depois do 01 | papéis `monitora_app` e `monitora_scraper` e permissões |
| `04_primeiro_admin.sql` | produção, 1 vez | cria o primeiro administrador (edite e-mail e senha antes) |
| `02_seed.sql` | **só desenvolvimento** | dados de teste (processo aberto, disciplinas, alunos) |
| `99_testes.sql` | **só banco de teste** | confere todas as regras e desfaz tudo (ROLLBACK) |

## Passo a passo — teste (faça isto primeiro)

1. Crie um banco novo e vazio (ex.: `monitora_teste`) e conecte nele.
2. Rode `01_schema.sql`, depois `03_setup_usuario.sql`.
3. Rode `99_testes.sql`. Na aba **Messages** deve aparecer
   `Regras do banco: OK` e `Permissões do monitora_app: OK`.
   Se aparecer `TESTE FALHOU: ...`, execute `ROLLBACK;` e me envie a mensagem.
4. (Opcional) Rode `02_seed.sql` para ter dados de exemplo no app em desenvolvimento.

> Se o banco já tiver tabelas de uma versão anterior, o `01` dá "relação já existe".
> Use um banco novo ou, se não houver dados a manter, `DROP SCHEMA public CASCADE;`
> seguido de `CREATE SCHEMA public;` e rode `01` e `03` de novo.

## Passo a passo — produção

1. Crie o banco vazio e rode `01_schema.sql`, depois `03_setup_usuario.sql`.
2. Defina as senhas dos papéis (em uma consulta separada, sem salvar o arquivo):
   `ALTER ROLE monitora_app PASSWORD '...';` e `ALTER ROLE monitora_scraper PASSWORD '...';`
3. Edite e rode `04_primeiro_admin.sql` (troque e-mail e senha pelos reais).
4. Configure o backend com `monitora_app` e o scraper com `monitora_scraper`.
5. **Não** rode `02_seed.sql` nem `99_testes.sql` em produção.

## Fluxo de cada semestre

1. O scraper carrega as disciplinas do SIGAA com o `semestre` (formato `AAAA/N`, ex.: `2026/2`).
2. O administrador cria o processo (nasce `AGENDADO`) e o abre (`ABERTO`).
   O banco só deixa abrir se já houver disciplinas daquele semestre.
3. Alunos se inscrevem; o professor decide; os e-mails são enviados e marcados.
4. O administrador encerra o processo (só com tudo decidido e enviado).
5. O administrador executa `SELECT limpar_processo_encerrado(<id_processo>);`
   — apaga alunos, inscrições, resultados, o processo e as disciplinas do semestre.
   **Irreversível**: o app deve pedir confirmação.

## Regras que o backend precisa respeitar

- **Autorização é do backend.** O banco usa um único papel para a aplicação; o backend
  deve autenticar o administrador (checando `ativo`) antes de qualquer ação administrativa.
- **Semestre** deve ser idêntico (`AAAA/N`) no processo, no scraper e nas disciplinas.
  O banco recusa outro formato.
- **Coeficiente** é enviado pelo backend e conferido pelo banco:
  `round(0,6 × IRA + 0,4 × nota)`, com MM = 3, MS = 4, SS = 5.
- **Um aluno = uma inscrição por processo.**
- **Um processo `ABERTO` por vez**; um segundo gera erro (traduzir para o usuário).
- **Chaves (`id_*`) são geradas pelo banco**: não enviar valor nos INSERTs.
- **Hash de senha:** o `04_primeiro_admin.sql` gera bcrypt. O login do backend precisa validar bcrypt.
- Datas de abertura/encerramento são **informativas**: nada abre ou fecha sozinho.
- Para registrar resultado, use `id_inscricao` da view `vw_inscricoes_pendentes`.
